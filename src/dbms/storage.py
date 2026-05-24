from __future__ import annotations

import os
import struct
import threading
from collections import OrderedDict
from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import BinaryIO, Iterator


from dbms.errors import (
    ColumnMismatchError,
    CorruptFileError,
    DuplicateTableError,
    RowNotFoundError,
    RowTooLargeError,
    TableNotFoundError,
    TypeMismatchError,
)
from dbms.storage_protocol import (
    ItemOffset,
    PageId,
    RowId,
    SBoolValue,
    SlotId,
    SIntValue,
    StorageColumnDef,
    StorageColumnType,
    StorageRow,
    STextValue,
    TableName,
)
from dbms.storage_utils import validate_storage_value

__all__ = [
    "FileStorage",
    "Page",
    "PageId",
    "SlotId",
    "TableMeta",
    "TableName",
    "PAGE_SIZE",
    "PAGE_TYPE_DATA",
    "PAGE_TYPE_META",
    "DEFAULT_PAGE_CACHE_SIZE",
]

PAGE_SIZE = 4096
PAGE_TYPE_META = 0
PAGE_TYPE_DATA = 1
HEADER_SIZE = 12
ITEMID_SIZE = 4
MAX_ITEM_SIZE = PAGE_SIZE - HEADER_SIZE - ITEMID_SIZE
DEFAULT_PAGE_CACHE_SIZE = 128

_thread_local = threading.local()


class _StorageRowSerializer:
    @staticmethod
    def serialize(row: StorageRow, col_types: Sequence[StorageColumnType]) -> bytes:
        buf = bytearray()
        for val, col_type in zip(row, col_types):
            if col_type == StorageColumnType.INT:
                assert isinstance(val, SIntValue)
                buf.extend(struct.pack("<i", val.value))
            elif col_type == StorageColumnType.BOOL:
                assert isinstance(val, SBoolValue)
                buf.append(0x01 if val.value else 0x00)
            elif col_type == StorageColumnType.TEXT:
                assert isinstance(val, STextValue)
                encoded = val.value.encode("utf-8")
                buf.extend(struct.pack("<H", len(encoded)))
                buf.extend(encoded)
        return bytes(buf)

    @staticmethod
    def deserialize(data: bytes, col_types: Sequence[StorageColumnType]) -> StorageRow:
        mv = memoryview(data)
        offset = 0
        cols: list[SIntValue | SBoolValue | STextValue] = []
        for col_type in col_types:
            if col_type == StorageColumnType.INT:
                val = struct.unpack_from("<i", mv, offset)[0]
                offset += 4
                cols.append(SIntValue(value=val))
            elif col_type == StorageColumnType.BOOL:
                byte_val = mv[offset]
                offset += 1
                cols.append(SBoolValue(value=byte_val != 0))
            elif col_type == StorageColumnType.TEXT:
                text_len = struct.unpack_from("<H", mv, offset)[0]
                offset += 2
                text = mv[offset : offset + text_len].tobytes().decode("utf-8")
                offset += text_len
                cols.append(STextValue(value=text))
        return tuple(cols)


@dataclass
class TableMeta:
    name: TableName
    columns: tuple[StorageColumnDef, ...]
    head_data_page: PageId

    @staticmethod
    def serialize(name: TableName, columns: tuple[StorageColumnDef, ...], head_data_page: PageId) -> bytes:
        name_bytes = name.encode("utf-8")
        total = 2 + len(name_bytes) + 2
        for cd in columns:
            col_bytes = cd.name.encode("utf-8")
            total += 2 + len(col_bytes) + 1
        total += 4
        buf = bytearray(total)
        struct.pack_into("<H", buf, 0, len(name_bytes))
        pos = 2
        buf[pos : pos + len(name_bytes)] = name_bytes
        pos += len(name_bytes)
        struct.pack_into("<H", buf, pos, len(columns))
        pos += 2
        for cd in columns:
            col_bytes = cd.name.encode("utf-8")
            struct.pack_into("<H", buf, pos, len(col_bytes))
            pos += 2
            buf[pos : pos + len(col_bytes)] = col_bytes
            pos += len(col_bytes)
            buf[pos] = cd.type.value
            pos += 1
        struct.pack_into("<I", buf, pos, head_data_page)
        return bytes(buf)

    @staticmethod
    def deserialize(data: bytes) -> "TableMeta":
        mv = memoryview(data)
        offset = 0
        name_len = struct.unpack_from("<H", mv, offset)[0]
        offset += 2
        name = TableName(mv[offset : offset + name_len].tobytes().decode("utf-8"))
        offset += name_len
        num_cols = struct.unpack_from("<H", mv, offset)[0]
        offset += 2
        columns: list[StorageColumnDef] = []
        for _ in range(num_cols):
            col_len = struct.unpack_from("<H", mv, offset)[0]
            offset += 2
            col_name = mv[offset : offset + col_len].tobytes().decode("utf-8")
            offset += col_len
            col_type_byte = mv[offset]
            offset += 1
            if col_type_byte == 0:
                col_type = StorageColumnType.INT
            elif col_type_byte == 1:
                col_type = StorageColumnType.BOOL
            elif col_type_byte == 2:
                col_type = StorageColumnType.TEXT
            else:
                raise CorruptFileError(f"Invalid column type byte: {col_type_byte}")
            columns.append(StorageColumnDef(name=col_name, type=col_type))
        head_data_page = PageId(struct.unpack_from("<I", mv, offset)[0])
        return TableMeta(name=name, columns=tuple(columns), head_data_page=head_data_page)


@dataclass
class PageHeader:
    page_type: int
    num_items: int
    pd_lower: ItemOffset
    pd_upper: ItemOffset
    next_page: PageId

    def serialize(self) -> bytes:
        return struct.pack(
            "<HHHHI",
            self.page_type,
            self.num_items,
            self.pd_lower,
            self.pd_upper,
            self.next_page,
        )

    @staticmethod
    def deserialize(data: bytes, offset: int = 0) -> tuple[PageHeader, int]:
        page_type, num_items, pd_lower, pd_upper, next_page = struct.unpack_from(
            "<HHHHI", data, offset
        )
        return (
            PageHeader(
                page_type=page_type,
                num_items=num_items,
                pd_lower=ItemOffset(pd_lower),
                pd_upper=ItemOffset(pd_upper),
                next_page=PageId(next_page),
            ),
            offset + HEADER_SIZE,
        )


@dataclass
class ItemId:
    offset: ItemOffset
    length: int


class _ItemView:
    __slots__ = ("_page",)

    def __init__(self, page: Page) -> None:
        self._page = page

    def __getitem__(self, i: int) -> bytes:
        if i >= len(self._page._items):
            raise IndexError(i)
        val = self._page._items[i]
        if val is not None:
            return val
        item_id = self._page.item_ids[i]
        if item_id.offset == ItemOffset(0):
            return b""
        assert self._page._raw is not None
        return self._page._raw[item_id.offset : item_id.offset + item_id.length]

    def __setitem__(self, i: int, v: bytes) -> None:
        self._page._items[i] = v

    def __len__(self) -> int:
        return len(self._page._items)

    def __iter__(self) -> Iterator[bytes]:
        for i in range(len(self._page._items)):
            yield self[i]

    def append(self, v: bytes) -> None:
        self._page._items.append(v)


class Page:
    __slots__ = ("header", "item_ids", "_items", "_raw", "_item_view")

    _items: list[bytes | None]

    def __init__(
        self,
        header: PageHeader,
        item_ids: list[ItemId],
        items: list[bytes],
        _raw: bytes | None = None,
    ) -> None:
        self.header = header
        self.item_ids = item_ids
        self._raw = _raw
        if _raw is not None:
            self._items = [None] * len(item_ids)
        else:
            self._items = list(items)
        self._item_view = _ItemView(self)

    @property
    def items(self) -> _ItemView:
        return self._item_view

    @items.setter
    def items(self, value: list[bytes | None]) -> None:
        self._items = value

    def is_deleted(self, slot_id: SlotId) -> bool:
        return self.item_ids[slot_id].offset == ItemOffset(0)

    def delete_item(self, slot_id: SlotId) -> None:
        self.item_ids[slot_id].offset = ItemOffset(0)
        self.item_ids[slot_id].length = 0
        self._items[slot_id] = b""

    def iter_nondeleted(self) -> Iterator[bytes]:
        for i, item_id in enumerate(self.item_ids):
            if item_id.offset != ItemOffset(0):
                yield self.items[i]

    @staticmethod
    def empty(page_type: int) -> Page:
        header = PageHeader(
            page_type=page_type,
            num_items=0,
            pd_lower=ItemOffset(HEADER_SIZE),
            pd_upper=ItemOffset(PAGE_SIZE),
            next_page=PageId(0),
        )
        return Page(header, [], [])

    def free_space(self) -> int:
        return self.header.pd_upper - self.header.pd_lower

    def add_item(self, item_bytes: bytes) -> None:
        offset = ItemOffset(self.header.pd_upper - len(item_bytes))
        item_id = ItemId(offset=offset, length=len(item_bytes))
        self.item_ids.append(item_id)
        self.items.append(item_bytes)
        self.header.num_items += 1
        self.header.pd_lower = ItemOffset(self.header.pd_lower + ITEMID_SIZE)
        self.header.pd_upper = offset

    def serialize(self) -> bytes:
        if not hasattr(_thread_local, "page_buffer"):
            _thread_local.page_buffer = bytearray(PAGE_SIZE)
        buf = _thread_local.page_buffer
        buf[:] = b"\x00" * PAGE_SIZE
        struct.pack_into(
            "<HHHHI",
            buf,
            0,
            self.header.page_type,
            self.header.num_items,
            self.header.pd_lower,
            self.header.pd_upper,
            self.header.next_page,
        )
        for i, item_id in enumerate(self.item_ids):
            struct.pack_into(
                "<HH",
                buf,
                HEADER_SIZE + i * ITEMID_SIZE,
                item_id.offset,
                item_id.length,
            )
        for i, item_id in enumerate(self.item_ids):
            if item_id.offset == ItemOffset(0):
                continue
            item_bytes = self.items[i]
            buf[item_id.offset : item_id.offset + item_id.length] = item_bytes
        return bytes(buf)

    @staticmethod
    def deserialize(data: bytes, page_num: PageId) -> Page:
        if len(data) < HEADER_SIZE:
            raise CorruptFileError(f"Page {page_num} too small")

        header, _ = PageHeader.deserialize(data, 0)

        if header.num_items < 0:
            raise CorruptFileError(f"Page {page_num}: negative num_items")
        if header.pd_lower < HEADER_SIZE or header.pd_lower > PAGE_SIZE:
            raise CorruptFileError(f"Page {page_num}: invalid pd_lower")
        if header.pd_upper > PAGE_SIZE:
            raise CorruptFileError(f"Page {page_num}: invalid pd_upper")
        if header.pd_lower > header.pd_upper:
            raise CorruptFileError(f"Page {page_num}: pd_lower > pd_upper")
        max_itemids_end = HEADER_SIZE + header.num_items * ITEMID_SIZE
        if header.pd_lower < max_itemids_end:
            raise CorruptFileError(
                f"Page {page_num}: pd_lower too small for num_items"
            )

        item_ids: list[ItemId] = []
        for i in range(header.num_items):
            off, length = struct.unpack_from(
                "<HH", data, HEADER_SIZE + i * ITEMID_SIZE
            )
            if off != 0:
                if off + length > PAGE_SIZE:
                    raise CorruptFileError(
                        f"Page {page_num}: item {i} out of bounds"
                    )
                if off < header.pd_upper:
                    raise CorruptFileError(
                        f"Page {page_num}: item {i} inside free space"
                    )
            item_ids.append(ItemId(offset=ItemOffset(off), length=length))

        return Page(header, item_ids, [], _raw=data)


class FileStorage:
    def __init__(
        self, path: Path, 
        max_page_cache_size: int = DEFAULT_PAGE_CACHE_SIZE,
        optimize_space: bool = False,
    ) -> None:
        self._path = path
        self._tables: dict[TableName, TableMeta] = {}
        self._page_cache: OrderedDict[PageId, Page] = OrderedDict()
        self._clean_pages: OrderedDict[PageId, None] = OrderedDict()
        self._dirty_pages: set[PageId] = set()
        self._pending_creates: dict[TableName, tuple[StorageColumnDef, ...]] = {}
        self._pending_inserts: dict[TableName, list[StorageRow]] = {}
        self._pending_updates: dict[TableName, dict[RowId, StorageRow]] = {}
        self._pending_deletes: dict[TableName, set[RowId]] = {}
        self._next_page_id: PageId = PageId(0)
        self._table_last_page: dict[TableName, PageId] = {}
        self._page_to_table: dict[PageId, TableName] = {}
        self._meta_last_page: PageId = PageId(0)
        self._max_page_cache_size = max_page_cache_size
        self._optimize_space = optimize_space

        exists = path.exists()
        if exists:
            file_size = path.stat().st_size
            if file_size % PAGE_SIZE != 0:
                raise CorruptFileError(
                    f"File size {file_size} not a multiple of page size {PAGE_SIZE}"
                )
            self._fd = open(path, "r+b")
            self._next_page_id = PageId(file_size // PAGE_SIZE)
            try:
                self._load_metadata()
            except Exception:
                self._fd.close()
                raise
        else:
            self._fd = open(path, "w+b")
            page0 = Page.empty(PAGE_TYPE_META)
            self._fd.write(page0.serialize())
            self._fd.flush()
            self._page_cache[PageId(0)] = page0
            self._clean_pages[PageId(0)] = None
            self._next_page_id = PageId(1)

    def _load_metadata(self) -> None:
        page_id = PageId(0)
        visited: set[PageId] = set()
        while True:
            if page_id in visited:
                raise CorruptFileError(
                    f"Metadata page cycle detected at page {page_id}"
                )
            if page_id >= self._next_page_id:
                raise CorruptFileError(
                    f"Metadata page {page_id} points beyond file"
                )
            visited.add(page_id)
            page = self._get_page(page_id)
            for item_bytes in page.iter_nondeleted():
                meta = TableMeta.deserialize(item_bytes)
                self._tables[meta.name] = meta
            next_page = page.header.next_page
            if next_page == PageId(0):
                self._meta_last_page = page_id
                break
            page_id = next_page

        for name, meta in self._tables.items():
            last_pid = meta.head_data_page
            self._page_to_table[last_pid] = name
            while True:
                page = self._get_page(last_pid)
                if page.header.next_page == PageId(0):
                    break
                last_pid = page.header.next_page
                self._page_to_table[last_pid] = name
            self._table_last_page[name] = last_pid

    def _require_table(self, name: TableName) -> TableMeta:
        if name not in self._tables:
            raise TableNotFoundError(name)
        return self._tables[name]

    def _evict_page(self, exclude: PageId | None = None) -> None:
        while len(self._page_cache) > self._max_page_cache_size:
            if not self._clean_pages:
                return
            page_id = next(iter(self._clean_pages))
            if page_id == exclude:
                if len(self._clean_pages) == 1:
                    return
                self._clean_pages.move_to_end(page_id)
                page_id = next(iter(self._clean_pages))
            del self._page_cache[page_id]
            del self._clean_pages[page_id]

    def _get_page(self, page_id: PageId) -> Page:
        if page_id < 0 or page_id >= self._next_page_id:
            raise CorruptFileError(
                f"Page {page_id} out of bounds (0..{self._next_page_id - 1})"
            )
        if page_id not in self._page_cache:
            self._fd.seek(page_id * PAGE_SIZE)
            data = self._fd.read(PAGE_SIZE)
            if len(data) < PAGE_SIZE:
                raise CorruptFileError(f"Page {page_id} read past EOF")
            self._page_cache[page_id] = Page.deserialize(data, page_id)
            self._clean_pages[page_id] = None
        self._page_cache.move_to_end(page_id)
        if page_id in self._clean_pages:
            self._clean_pages.move_to_end(page_id)
        self._evict_page(exclude=page_id)
        return self._page_cache[page_id]

    def _mark_dirty(self, page_id: PageId) -> None:
        self._dirty_pages.add(page_id)
        self._clean_pages.pop(page_id, None)

    def _allocate_page_id(self) -> PageId:
        pid = self._next_page_id
        self._next_page_id = PageId(self._next_page_id + 1)
        return pid

    def _allocate_page(self, page_type: int) -> PageId:
        pid = self._allocate_page_id()
        page = Page.empty(page_type)
        self._page_cache[pid] = page
        self._page_cache.move_to_end(pid)
        self._mark_dirty(pid)
        self._evict_page()
        return pid

    def _write_page(self, page_id: PageId) -> None:
        page = self._page_cache.get(page_id)
        if page is None:
            return
        self._fd.seek(page_id * PAGE_SIZE)
        self._fd.write(page.serialize())

    def _append_data_page(self, table_name: TableName) -> PageId:
        old_last = self._table_last_page.get(table_name)
        new_pid = self._allocate_page(PAGE_TYPE_DATA)
        self._page_to_table[new_pid] = table_name
        if old_last is not None:
            last_page = self._get_page(old_last)
            last_page.header.next_page = new_pid
            self._mark_dirty(old_last)
        self._table_last_page[table_name] = new_pid
        return new_pid

    def _find_space_in_table(self, table_name: TableName, needed: int) -> PageId | None:
        last_pid = self._table_last_page.get(table_name)
        if last_pid is not None:
            page = self._get_page(last_pid)
            if page.free_space() >= needed:
                return last_pid
        if not self._optimize_space:
            return None
        meta = self._tables[table_name]
        page_id = meta.head_data_page
        while page_id != PageId(0):
            page = self._get_page(page_id)
            if page.free_space() >= needed:
                return page_id
            page_id = page.header.next_page
        return None

    def _ensure_data_page(self, table_name: TableName, needed: int) -> PageId:
        found = self._find_space_in_table(table_name, needed)
        if found is not None:
            return found
        return self._append_data_page(table_name)

    def create_table(self, name: TableName, columns: Sequence[StorageColumnDef]) -> None:
        if name in self._tables:
            raise DuplicateTableError(name)
        head_pid = self._allocate_page(PAGE_TYPE_DATA)
        self._page_to_table[head_pid] = name
        self._tables[name] = TableMeta(
            name=name, columns=tuple(columns), head_data_page=head_pid
        )
        self._table_last_page[name] = head_pid
        self._pending_creates[name] = tuple(columns)

    def table_exists(self, name: TableName) -> bool:
        return name in self._tables

    def get_columns(self, name: TableName) -> Sequence[StorageColumnDef]:
        meta = self._require_table(name)
        return meta.columns

    def get_tables(self) -> Sequence[TableName]:
        return list(self._tables.keys())

    def insert_row(self, table: TableName, row: StorageRow) -> None:
        meta = self._require_table(table)
        storage_cols = meta.columns
        if len(row) != len(storage_cols):
            raise ColumnMismatchError(
                f"Expected {len(storage_cols)} values, got {len(row)}"
            )
        for i, (val, col_def) in enumerate(zip(row, storage_cols)):
            validate_storage_value(val, col_def, storage_cols[i].name)

        row_bytes = _StorageRowSerializer.serialize(row, tuple(cd.type for cd in storage_cols))
        if len(row_bytes) > MAX_ITEM_SIZE:
            raise RowTooLargeError(
                f"Row size {len(row_bytes)} exceeds max {MAX_ITEM_SIZE}"
            )
        self._pending_inserts.setdefault(table, []).append(row)

    def scan_rows(self, table: TableName) -> Iterator[tuple[RowId, StorageRow]]:
        self._require_table(table)
        meta = self._tables[table]
        col_types = tuple(cd.type for cd in meta.columns)
        page_id = meta.head_data_page
        while page_id != PageId(0):
            page = self._get_page(page_id)
            for i in range(len(page.item_ids)):
                if page.is_deleted(SlotId(i)):
                    continue
                row = _StorageRowSerializer.deserialize(page.items[i], col_types)
                yield ((page_id, SlotId(i)), row)
            page_id = page.header.next_page

    def mark_update(self, table: TableName, row_id: RowId, new_row: StorageRow) -> None:
        meta = self._require_table(table)
        storage_cols = meta.columns
        if len(new_row) != len(storage_cols):
            raise ColumnMismatchError(
                f"Expected {len(storage_cols)} values, got {len(new_row)}"
            )
        for i, (val, col_def) in enumerate(zip(new_row, storage_cols)):
            validate_storage_value(val, col_def, storage_cols[i].name)

        page_id, slot_id = row_id
        if page_id in self._page_to_table:
            actual_table = self._page_to_table[page_id]
            if actual_table != table:
                raise RowNotFoundError(
                    f"RowId ({page_id}, {slot_id}) belongs to table '{actual_table}', not '{table}'"
                )
        self._pending_updates.setdefault(table, {})[row_id] = new_row

    def mark_delete(self, table: TableName, row_id: RowId) -> None:
        self._require_table(table)
        page_id, slot_id = row_id
        if page_id in self._page_to_table:
            actual_table = self._page_to_table[page_id]
            if actual_table != table:
                raise RowNotFoundError(
                    f"RowId ({page_id}, {slot_id}) belongs to table '{actual_table}', not '{table}'"
                )
        self._pending_deletes.setdefault(table, set()).add(row_id)

    def commit(self) -> None:
        self._apply_pending_operations()
        self._write_metadata_if_needed()
        self._flush_dirty_pages()
        self._clear_pending_state()

    def _apply_pending_operations(self) -> None:
        for table_name, rows in self._pending_inserts.items():
            storage_cols = self._tables[table_name].columns
            col_types = tuple(cd.type for cd in storage_cols)
            for row in rows:
                row_bytes = _StorageRowSerializer.serialize(row, col_types)
                needed = ITEMID_SIZE + len(row_bytes)
                page_id = self._ensure_data_page(table_name, needed)
                page = self._get_page(page_id)
                page.add_item(row_bytes)
                self._mark_dirty(page_id)

        for table_name, updates in self._pending_updates.items():
            storage_cols = self._tables[table_name].columns
            col_types = tuple(cd.type for cd in storage_cols)
            deletes = self._pending_deletes.get(table_name, set())
            for rid, new_row in updates.items():
                if rid in deletes:
                    continue
                page_id, slot_id = rid
                page = self._get_page(page_id)
                if slot_id >= len(page.item_ids):
                    raise RowNotFoundError(
                        f"Invalid RowId ({page_id}, {slot_id}) for table {table_name}"
                    )
                if page.is_deleted(slot_id):
                    raise RowNotFoundError(
                        f"RowId ({page_id}, {slot_id}) already deleted in table {table_name}"
                    )
                item_id = page.item_ids[slot_id]
                new_bytes = _StorageRowSerializer.serialize(new_row, col_types)
                if len(new_bytes) <= item_id.length:
                    page.items[slot_id] = new_bytes
                    item_id.length = len(new_bytes)
                    self._mark_dirty(page_id)
                else:
                    if len(new_bytes) > MAX_ITEM_SIZE:
                        raise RowTooLargeError(
                            f"Row size {len(new_bytes)} exceeds max {MAX_ITEM_SIZE}"
                        )
                    page.delete_item(slot_id)
                    needed = ITEMID_SIZE + len(new_bytes)
                    target_pid = self._ensure_data_page(table_name, needed)
                    target_page = self._get_page(target_pid)
                    target_page.add_item(new_bytes)
                    self._mark_dirty(target_pid)
                    self._mark_dirty(page_id)

        for table_name, row_ids in self._pending_deletes.items():
            for rid in row_ids:
                page_id, slot_id = rid
                page = self._get_page(page_id)
                if slot_id >= len(page.item_ids):
                    raise RowNotFoundError(
                        f"Invalid RowId ({page_id}, {slot_id}) for table {table_name}"
                    )
                if page.is_deleted(slot_id):
                    raise RowNotFoundError(
                        f"RowId ({page_id}, {slot_id}) already deleted in table {table_name}"
                    )
                page.delete_item(slot_id)
                self._mark_dirty(page_id)

    @staticmethod
    def _count_metadata_pages(metas: list[TableMeta]) -> int:
        count = 1
        free = Page.empty(PAGE_TYPE_META).free_space()
        for meta in metas:
            meta_bytes = TableMeta.serialize(meta.name, meta.columns, PageId(0))
            needed = ITEMID_SIZE + len(meta_bytes)
            if free < needed:
                count += 1
                free = Page.empty(PAGE_TYPE_META).free_space() - needed
            else:
                free -= needed
        return count

    def _flush_dirty_pages(self) -> None:
        for pid in sorted(self._dirty_pages):
            self._write_page(pid)
            if pid in self._page_cache:
                self._clean_pages[pid] = None
        self._fd.flush()
        os.fsync(self._fd.fileno())

    def _clear_pending_state(self) -> None:
        self._dirty_pages.clear()
        self._pending_creates.clear()
        self._pending_inserts.clear()
        self._pending_updates.clear()
        self._pending_deletes.clear()

    def _write_metadata_if_needed(self) -> None:
        if not self._pending_creates:
            return
        for name in list(self._pending_creates.keys()):
            meta = self._tables[name]
            meta_bytes = TableMeta.serialize(
                meta.name, meta.columns, meta.head_data_page
            )
            self._add_item_to_meta_chain(meta_bytes)

    def _add_item_to_meta_chain(self, meta_bytes: bytes) -> None:
        if len(meta_bytes) > MAX_ITEM_SIZE:
            raise RowTooLargeError(
                f"Metadata size {len(meta_bytes)} exceeds max {MAX_ITEM_SIZE}"
            )
        needed = ITEMID_SIZE + len(meta_bytes)
        page_id = self._meta_last_page
        page = self._get_page(page_id)
        if page.free_space() >= needed:
            page.add_item(meta_bytes)
            self._mark_dirty(page_id)
        else:
            new_pid = self._allocate_page(PAGE_TYPE_META)
            page.header.next_page = new_pid
            self._mark_dirty(page_id)
            new_page = self._get_page(new_pid)
            new_page.add_item(meta_bytes)
            self._mark_dirty(new_pid)
            self._meta_last_page = new_pid

    def _write_metadata_to_fd(self, fd: BinaryIO, metas: list[TableMeta]) -> PageId:
        meta_page = Page.empty(PAGE_TYPE_META)
        current_pid = PageId(0)

        for meta in metas:
            meta_bytes = TableMeta.serialize(
                meta.name, meta.columns, meta.head_data_page
            )
            needed = ITEMID_SIZE + len(meta_bytes)
            if meta_page.free_space() < needed:
                fd.seek(current_pid * PAGE_SIZE)
                new_pid = PageId(current_pid + 1)
                meta_page.header.next_page = new_pid
                fd.write(meta_page.serialize())
                meta_page = Page.empty(PAGE_TYPE_META)
                current_pid = new_pid
            meta_page.add_item(meta_bytes)

        fd.seek(current_pid * PAGE_SIZE)
        fd.write(meta_page.serialize())
        return current_pid

    def _vacuum_stream_table(
        self, name: TableName, fd: BinaryIO, running_pid: PageId
    ) -> tuple[PageId, PageId, PageId]:
        meta = self._tables[name]
        src_page_id = meta.head_data_page
        head_pid = running_pid

        current_out_page = Page.empty(PAGE_TYPE_DATA)
        current_out_pid = running_pid
        running_pid = PageId(running_pid + 1)

        while src_page_id != PageId(0):
            src_page = self._get_page(src_page_id)
            for item_bytes in src_page.iter_nondeleted():
                needed = ITEMID_SIZE + len(item_bytes)
                if current_out_page.free_space() < needed:
                    current_out_page.header.next_page = running_pid
                    fd.seek(current_out_pid * PAGE_SIZE)
                    fd.write(current_out_page.serialize())
                    current_out_pid = running_pid
                    running_pid = PageId(running_pid + 1)
                    current_out_page = Page.empty(PAGE_TYPE_DATA)
                current_out_page.add_item(item_bytes)
            src_page_id = src_page.header.next_page

        fd.seek(current_out_pid * PAGE_SIZE)
        fd.write(current_out_page.serialize())

        return head_pid, current_out_pid, running_pid

    def _vacuum_build_compacted_file(
        self,
        tmp_fd: BinaryIO,
        table_order: list[TableName],
        table_columns: dict[TableName, tuple[StorageColumnDef, ...]],
        num_meta_pages: int,
    ) -> tuple[list[TableMeta], dict[TableName, PageId], PageId, PageId]:
        tmp_fd.write(b"\x00" * (num_meta_pages * PAGE_SIZE))

        running_pid = PageId(num_meta_pages)
        table_heads: dict[TableName, PageId] = {}
        table_last_pids: dict[TableName, PageId] = {}

        for name in table_order:
            head_pid, last_pid, running_pid = self._vacuum_stream_table(
                name, tmp_fd, running_pid
            )
            table_heads[name] = head_pid
            table_last_pids[name] = last_pid

        final_metas = [
            TableMeta(
                name=n,
                columns=table_columns[n],
                head_data_page=table_heads[n],
            )
            for n in table_order
        ]

        meta_last_pid = self._write_metadata_to_fd(tmp_fd, final_metas)
        return final_metas, table_last_pids, running_pid, meta_last_pid

    def _vacuum_swap_files(self, tmp_path: Path) -> None:
        self._fd.close()
        tmp_path.replace(self._path)
        self._fd = open(self._path, "r+b")

    def vacuum(self) -> None:
        self.commit()

        table_order = list(self._tables.keys())
        table_columns = {name: self._tables[name].columns for name in table_order}

        meta_list = [
            TableMeta(name=n, columns=table_columns[n], head_data_page=PageId(0))
            for n in table_order
        ]
        num_meta_pages = self._count_metadata_pages(meta_list)

        tmp_path = self._path.with_suffix(".db.tmp")
        tmp_fd = open(tmp_path, "w+b")

        try:
            final_metas, table_last_pids, next_page_id, meta_last_pid = (
                self._vacuum_build_compacted_file(
                    tmp_fd, table_order, table_columns, num_meta_pages
                )
            )
            tmp_fd.flush()
            os.fsync(tmp_fd.fileno())
            tmp_fd.close()
        except BaseException:
            tmp_fd.close()
            tmp_path.unlink(missing_ok=True)
            raise

        self._vacuum_swap_files(tmp_path)

        self._page_cache.clear()
        self._clean_pages.clear()
        self._dirty_pages.clear()
        self._tables = {m.name: m for m in final_metas}
        self._table_last_page = table_last_pids
        self._next_page_id = next_page_id
        self._meta_last_page = meta_last_pid
        self._page_to_table.clear()
        for name, meta in self._tables.items():
            page_id = meta.head_data_page
            while page_id != PageId(0):
                self._page_to_table[page_id] = name
                page = self._get_page(page_id)
                page_id = page.header.next_page
        self._clear_pending_state()

    def close(self) -> None:
        self._flush_dirty_pages()
        self._fd.close()

    def __enter__(self) -> "FileStorage":
        return self

    def __exit__(self, *args: object) -> None:
        self.close()
