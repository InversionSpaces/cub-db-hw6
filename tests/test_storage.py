import signal
import struct

import pytest
from pathlib import Path

from dbms.ast_nodes import IntValue, TextValue, BoolValue
from dbms.errors import (
    ColumnMismatchError,
    CorruptFileError,
    DuplicateTableError,
    RowTooLargeError,
    TableNotFoundError,
    TypeMismatchError,
)
from dbms.storage import (
    FileStorage,
    Page,
    PageId,
    SlotId,
    TableMeta,
    TableName,
    PAGE_SIZE,
    PAGE_TYPE_DATA,
    PAGE_TYPE_META,
    _StorageRowSerializer,
)
from dbms.storage_protocol import SBoolValue, SIntValue, StorageColumnDef, StorageColumnType, StorageRow, STextValue
from dbms.in_memory_storage import InMemoryStorage


def _scd(name: str, stype: StorageColumnType = StorageColumnType.TEXT) -> StorageColumnDef:
    return StorageColumnDef(name=name, type=stype)


def _t(v: str) -> STextValue:
    return STextValue(value=v)


def _i(v: int) -> SIntValue:
    return SIntValue(value=v)


def _b(v: bool) -> SBoolValue:
    return SBoolValue(value=v)


@pytest.fixture
def store() -> InMemoryStorage:
    return InMemoryStorage()


@pytest.fixture
def file_store(tmp_path: Path) -> FileStorage:
    return FileStorage(tmp_path / "test.db")


def _rows_per_page(payload: str) -> int:
    row_bytes: bytes = _StorageRowSerializer.serialize((_t(payload),), (StorageColumnType.TEXT,))
    page = Page.empty(PAGE_TYPE_DATA)
    free_before: int = page.free_space()
    page.add_item(row_bytes)
    per_item: int = free_before - page.free_space()
    return free_before // per_item


def _tables_per_meta_page(name: str, columns: tuple[StorageColumnDef, ...]) -> int:
    meta_bytes: bytes = TableMeta.serialize(TableName(name), columns, PageId(1))
    page = Page.empty(PAGE_TYPE_META)
    free_before: int = page.free_space()
    page.add_item(meta_bytes)
    per_item: int = free_before - page.free_space()
    return free_before // per_item


class TestCreateTable:
    def test_create_and_scan(self, store: InMemoryStorage) -> None:
        store.create_table(TableName("t"), (_scd("a"), _scd("b")))
        store.insert_row(TableName("t"), (_t("x"), _t("y")))
        rows = list(store.scan_rows(TableName("t")))
        assert len(rows) == 1

    def test_duplicate_table_raises(self, store: InMemoryStorage) -> None:
        store.create_table(TableName("t"), (_scd("a"),))
        with pytest.raises(DuplicateTableError):
            store.create_table(TableName("t"), (_scd("b"),))

    def test_get_columns(self, store: InMemoryStorage) -> None:
        store.create_table(TableName("t"), (_scd("x"), _scd("y"), _scd("z")))
        cols = store.get_columns(TableName("t"))
        assert len(cols) == 3
        assert cols[0].name == "x"
        assert cols[0].type == StorageColumnType.TEXT
        assert cols[1].name == "y"
        assert cols[2].name == "z"

    def test_get_columns_missing_table(self, store: InMemoryStorage) -> None:
        with pytest.raises(TableNotFoundError):
            store.get_columns(TableName("missing"))

    def test_table_exists(self, store: InMemoryStorage) -> None:
        assert not store.table_exists(TableName("t"))
        store.create_table(TableName("t"), (_scd("a"),))
        assert store.table_exists(TableName("t"))


class TestInsertRow:
    def test_insert_and_scan(self, store: InMemoryStorage) -> None:
        store.create_table(TableName("t"), (_scd("a"), _scd("b")))
        store.insert_row(TableName("t"), (_t("x"), _t("y")))
        rows = list(store.scan_rows(TableName("t")))
        assert len(rows) == 1
        _, row = rows[0]
        assert row == (_t("x"), _t("y"))

    def test_insert_multiple_rows(self, store: InMemoryStorage) -> None:
        store.create_table(TableName("t"), (_scd("a"),))
        store.insert_row(TableName("t"), (_t("1"),))
        store.insert_row(TableName("t"), (_t("2"),))
        store.insert_row(TableName("t"), (_t("3"),))
        rows = list(store.scan_rows(TableName("t")))
        assert len(rows) == 3
        values = {r[1][0].value for r in rows}
        assert values == {"1", "2", "3"}

    def test_insert_missing_table(self, store: InMemoryStorage) -> None:
        with pytest.raises(TableNotFoundError):
            store.insert_row(TableName("missing"), (_t("x"),))

    def test_insert_column_mismatch(self, store: InMemoryStorage) -> None:
        store.create_table(TableName("t"), (_scd("a"), _scd("b")))
        with pytest.raises(ColumnMismatchError):
            store.insert_row(TableName("t"), (_t("x"),))

    def test_insert_duplicate_values(self, store: InMemoryStorage) -> None:
        store.create_table(TableName("t"), (_scd("a"),))
        store.insert_row(TableName("t"), (_t("x"),))
        store.insert_row(TableName("t"), (_t("x"),))
        assert len(list(store.scan_rows(TableName("t")))) == 2

    def test_insert_after_delete(self, store: InMemoryStorage) -> None:
        store.create_table(TableName("t"), (_scd("a"),))
        store.insert_row(TableName("t"), (_t("x"),))
        rid, _ = list(store.scan_rows(TableName("t")))[0]
        store.mark_delete(TableName("t"), rid)
        store.commit()
        store.insert_row(TableName("t"), (_t("y"),))
        rows = list(store.scan_rows(TableName("t")))
        assert len(rows) == 1
        assert rows[0][1] == (_t("y"),)


class TestScanRows:
    def test_scan_empty_table(self, store: InMemoryStorage) -> None:
        store.create_table(TableName("t"), (_scd("a"),))
        assert list(store.scan_rows(TableName("t"))) == []

    def test_scan_missing_table(self, store: InMemoryStorage) -> None:
        with pytest.raises(TableNotFoundError):
            list(store.scan_rows(TableName("missing")))


class TestMarkUpdateCommit:
    def test_update_and_commit(self, store: InMemoryStorage) -> None:
        store.create_table(TableName("t"), (_scd("a"),))
        store.insert_row(TableName("t"), (_t("x"),))
        rid, _ = list(store.scan_rows(TableName("t")))[0]
        store.mark_update(TableName("t"), rid, (_t("z"),))
        _, row = list(store.scan_rows(TableName("t")))[0]
        assert row == (_t("x"),)
        store.commit()
        _, row = list(store.scan_rows(TableName("t")))[0]
        assert row == (_t("z"),)

    def test_update_not_visible_before_commit(self, store: InMemoryStorage) -> None:
        store.create_table(TableName("t"), (_scd("a"),))
        store.insert_row(TableName("t"), (_t("x"),))
        rid, _ = list(store.scan_rows(TableName("t")))[0]
        store.mark_update(TableName("t"), rid, (_t("z"),))
        _, row = list(store.scan_rows(TableName("t")))[0]
        assert row == (_t("x"),)

    def test_multiple_updates_last_write_wins(self, store: InMemoryStorage) -> None:
        store.create_table(TableName("t"), (_scd("a"),))
        store.insert_row(TableName("t"), (_t("x"),))
        rid, _ = list(store.scan_rows(TableName("t")))[0]
        store.mark_update(TableName("t"), rid, (_t("y"),))
        store.mark_update(TableName("t"), rid, (_t("z"),))
        store.commit()
        _, row = list(store.scan_rows(TableName("t")))[0]
        assert row == (_t("z"),)

    def test_update_multiple_rows(self, store: InMemoryStorage) -> None:
        store.create_table(TableName("t"), (_scd("a"),))
        store.insert_row(TableName("t"), (_t("1"),))
        store.insert_row(TableName("t"), (_t("2"),))
        rows = list(store.scan_rows(TableName("t")))
        store.mark_update(TableName("t"), rows[0][0], (_t("x"),))
        store.mark_update(TableName("t"), rows[1][0], (_t("y"),))
        store.commit()
        values = {r[1][0].value for r in store.scan_rows(TableName("t"))}
        assert values == {"x", "y"}

    def test_update_deleted_row_skipped(self, store: InMemoryStorage) -> None:
        store.create_table(TableName("t"), (_scd("a"),))
        store.insert_row(TableName("t"), (_t("x"),))
        rid, _ = list(store.scan_rows(TableName("t")))[0]
        store.mark_delete(TableName("t"), rid)
        store.mark_update(TableName("t"), rid, (_t("z"),))
        store.commit()
        assert len(list(store.scan_rows(TableName("t")))) == 0

    def test_update_column_mismatch(self, store: InMemoryStorage) -> None:
        store.create_table(TableName("t"), (_scd("a"), _scd("b")))
        store.insert_row(TableName("t"), (_t("x"), _t("y")))
        rid, _ = list(store.scan_rows(TableName("t")))[0]
        with pytest.raises(ColumnMismatchError):
            store.mark_update(TableName("t"), rid, (_t("z"),))

    def test_update_missing_table(self, store: InMemoryStorage) -> None:
        with pytest.raises(TableNotFoundError):
            store.mark_update(TableName("missing"), (PageId(0), SlotId(0)), (_t("z"),))


class TestMarkDeleteCommit:
    def test_delete_and_commit(self, store: InMemoryStorage) -> None:
        store.create_table(TableName("t"), (_scd("a"),))
        store.insert_row(TableName("t"), (_t("x"),))
        store.insert_row(TableName("t"), (_t("y"),))
        rid = list(store.scan_rows(TableName("t")))[0][0]
        store.mark_delete(TableName("t"), rid)
        assert len(list(store.scan_rows(TableName("t")))) == 2
        store.commit()
        assert len(list(store.scan_rows(TableName("t")))) == 1

    def test_delete_multiple_rows(self, store: InMemoryStorage) -> None:
        store.create_table(TableName("t"), (_scd("a"),))
        store.insert_row(TableName("t"), (_t("1"),))
        store.insert_row(TableName("t"), (_t("2"),))
        store.insert_row(TableName("t"), (_t("3"),))
        rows = list(store.scan_rows(TableName("t")))
        store.mark_delete(TableName("t"), rows[0][0])
        store.mark_delete(TableName("t"), rows[1][0])
        store.commit()
        assert len(list(store.scan_rows(TableName("t")))) == 1

    def test_delete_not_visible_before_commit(self, store: InMemoryStorage) -> None:
        store.create_table(TableName("t"), (_scd("a"),))
        store.insert_row(TableName("t"), (_t("x"),))
        rid, _ = list(store.scan_rows(TableName("t")))[0]
        store.mark_delete(TableName("t"), rid)
        assert len(list(store.scan_rows(TableName("t")))) == 1

    def test_delete_missing_table(self, store: InMemoryStorage) -> None:
        with pytest.raises(TableNotFoundError):
            store.mark_delete(TableName("missing"), (PageId(0), SlotId(0)))


class TestCommitWithUpdatesAndDeletes:
    def test_update_and_delete_different_rows(self, store: InMemoryStorage) -> None:
        store.create_table(TableName("t"), (_scd("a"),))
        store.insert_row(TableName("t"), (_t("keep"),))
        store.insert_row(TableName("t"), (_t("delete"),))
        rows = list(store.scan_rows(TableName("t")))
        store.mark_update(TableName("t"), rows[0][0], (_t("updated"),))
        store.mark_delete(TableName("t"), rows[1][0])
        store.commit()
        rows = list(store.scan_rows(TableName("t")))
        assert len(rows) == 1
        assert rows[0][1] == (_t("updated"),)

    def test_commit_clears_pending(self, store: InMemoryStorage) -> None:
        store.create_table(TableName("t"), (_scd("a"),))
        store.insert_row(TableName("t"), (_t("x"),))
        rid, _ = list(store.scan_rows(TableName("t")))[0]
        store.mark_update(TableName("t"), rid, (_t("y"),))
        store.commit()
        store.mark_delete(TableName("t"), rid)
        store.commit()
        assert len(list(store.scan_rows(TableName("t")))) == 0

    def test_empty_commit_is_noop(self, store: InMemoryStorage) -> None:
        store.create_table(TableName("t"), (_scd("a"),))
        store.insert_row(TableName("t"), (_t("x"),))
        store.commit()
        assert len(list(store.scan_rows(TableName("t")))) == 1


class TestRowSerialization:
    def test_roundtrip_single_col(self) -> None:
        row = (_t("hello"),)
        col_types = (StorageColumnType.TEXT,)
        assert _StorageRowSerializer.deserialize(_StorageRowSerializer.serialize(row, col_types), col_types) == row

    def test_roundtrip_multi_col(self) -> None:
        row = (_t("abc"), _t("def"), _t("ghi"))
        col_types = (StorageColumnType.TEXT, StorageColumnType.TEXT, StorageColumnType.TEXT)
        assert _StorageRowSerializer.deserialize(_StorageRowSerializer.serialize(row, col_types), col_types) == row

    def test_roundtrip_empty_string(self) -> None:
        row = (_t(""),)
        col_types = (StorageColumnType.TEXT,)
        assert _StorageRowSerializer.deserialize(_StorageRowSerializer.serialize(row, col_types), col_types) == row

    def test_roundtrip_unicode(self) -> None:
        row = (_t("日本語"), _t("emoji🎉"))
        col_types = (StorageColumnType.TEXT, StorageColumnType.TEXT)
        assert _StorageRowSerializer.deserialize(_StorageRowSerializer.serialize(row, col_types), col_types) == row

    def test_roundtrip_long_string(self) -> None:
        row = (_t("x" * 500),)
        col_types = (StorageColumnType.TEXT,)
        assert _StorageRowSerializer.deserialize(_StorageRowSerializer.serialize(row, col_types), col_types) == row

    def test_roundtrip_int(self) -> None:
        row = (_i(42),)
        col_types = (StorageColumnType.INT,)
        result = _StorageRowSerializer.deserialize(_StorageRowSerializer.serialize(row, col_types), col_types)
        assert result == row

    def test_roundtrip_bool(self) -> None:
        row = (_b(True), _b(False))
        col_types = (StorageColumnType.BOOL, StorageColumnType.BOOL)
        assert _StorageRowSerializer.deserialize(_StorageRowSerializer.serialize(row, col_types), col_types) == row

    def test_roundtrip_mixed_types(self) -> None:
        row = (_i(123), _b(True), _t("hello"))
        col_types = (StorageColumnType.INT, StorageColumnType.BOOL, StorageColumnType.TEXT)
        assert _StorageRowSerializer.deserialize(_StorageRowSerializer.serialize(row, col_types), col_types) == row

    def test_int_serialization_format(self) -> None:
        row = (_i(-42),)
        col_types = (StorageColumnType.INT,)
        data = _StorageRowSerializer.serialize(row, col_types)
        assert len(data) == 4

    def test_bool_serialization_format(self) -> None:
        row = (_b(True),)
        col_types = (StorageColumnType.BOOL,)
        data = _StorageRowSerializer.serialize(row, col_types)
        assert len(data) == 1
        assert data == b'\x01'
        row2 = (_b(False),)
        data2 = _StorageRowSerializer.serialize(row2, col_types)
        assert data2 == b'\x00'

    def test_text_serialization_format(self) -> None:
        row = (_t("hi"),)
        col_types = (StorageColumnType.TEXT,)
        data = _StorageRowSerializer.serialize(row, col_types)
        assert data[:2] == struct.pack("<H", 2)
        assert data[2:] == b"hi"


class TestTableDefSerialization:
    def test_roundtrip_simple(self) -> None:
        columns = (_scd("name"), _scd("age"))
        data = TableMeta.serialize(TableName("users"), columns, PageId(1))
        meta = TableMeta.deserialize(data)
        assert meta.name == "users"
        assert len(meta.columns) == 2
        assert meta.columns[0].name == "name"
        assert meta.columns[0].type == StorageColumnType.TEXT
        assert meta.columns[1].name == "age"
        assert meta.columns[1].type == StorageColumnType.TEXT
        assert meta.head_data_page == 1

    def test_roundtrip_single_col(self) -> None:
        columns = (_scd("a"),)
        data = TableMeta.serialize(TableName("t"), columns, PageId(0))
        meta = TableMeta.deserialize(data)
        assert meta.name == "t"
        assert len(meta.columns) == 1
        assert meta.columns[0].name == "a"
        assert meta.head_data_page == 0

    def test_roundtrip_unicode_name(self) -> None:
        columns = (_scd("列1"), _scd("列2"))
        data = TableMeta.serialize(TableName("テーブル"), columns, PageId(5))
        meta = TableMeta.deserialize(data)
        assert meta.name == "テーブル"
        assert len(meta.columns) == 2
        assert meta.head_data_page == 5

    def test_roundtrip_with_types(self) -> None:
        columns = (
            _scd("id", StorageColumnType.INT),
            _scd("active", StorageColumnType.BOOL),
            _scd("name", StorageColumnType.TEXT),
        )
        data = TableMeta.serialize(TableName("t"), columns, PageId(1))
        meta = TableMeta.deserialize(data)
        assert meta.name == "t"
        assert len(meta.columns) == 3
        assert meta.columns[0].type == StorageColumnType.INT
        assert meta.columns[1].type == StorageColumnType.BOOL
        assert meta.columns[2].type == StorageColumnType.TEXT


class TestPageRoundtrip:
    def test_empty_page_roundtrip(self) -> None:
        page = Page.empty(PAGE_TYPE_DATA)
        data = page.serialize()
        assert len(data) == PAGE_SIZE
        restored = Page.deserialize(data, PageId(0))
        assert restored.header.page_type == PAGE_TYPE_DATA
        assert restored.header.num_items == 0
        assert len(restored.items) == 0

    def test_page_with_items_roundtrip(self) -> None:
        page = Page.empty(PAGE_TYPE_DATA)
        row_bytes = _StorageRowSerializer.serialize((_t("hello"), _t("world")), (StorageColumnType.TEXT, StorageColumnType.TEXT))
        page.add_item(row_bytes)
        row_bytes2 = _StorageRowSerializer.serialize((_t("foo"),), (StorageColumnType.TEXT,))
        page.add_item(row_bytes2)
        data = page.serialize()
        restored = Page.deserialize(data, PageId(0))
        assert restored.header.num_items == 2
        assert len(restored.items) == 2
        assert _StorageRowSerializer.deserialize(restored.items[0], (StorageColumnType.TEXT, StorageColumnType.TEXT)) == (_t("hello"), _t("world"))
        assert _StorageRowSerializer.deserialize(restored.items[1], (StorageColumnType.TEXT,)) == (_t("foo"),)

    def test_metadata_page_roundtrip(self) -> None:
        page = Page.empty(PAGE_TYPE_META)
        columns = (_scd("name"), _scd("age"))
        item = TableMeta.serialize(TableName("users"), columns, PageId(1))
        page.add_item(item)
        data = page.serialize()
        restored = Page.deserialize(data, PageId(0))
        assert restored.header.page_type == PAGE_TYPE_META
        assert len(restored.items) == 1
        meta = TableMeta.deserialize(restored.items[0])
        assert meta.name == "users"
        assert len(meta.columns) == 2
        assert meta.head_data_page == 1

    def test_free_space_tracking(self) -> None:
        page = Page.empty(PAGE_TYPE_DATA)
        assert page.free_space() == PAGE_SIZE - 12
        row_bytes = _StorageRowSerializer.serialize((_t("a"),), (StorageColumnType.TEXT,))
        page.add_item(row_bytes)
        assert page.free_space() == PAGE_SIZE - 12 - 4 - len(row_bytes)

    def test_corrupt_page_raises(self) -> None:
        page = Page.empty(PAGE_TYPE_DATA)
        data = bytearray(page.serialize())
        struct.pack_into("<H", data, 4, 3000)
        struct.pack_into("<H", data, 6, 2000)
        with pytest.raises(CorruptFileError):
            Page.deserialize(bytes(data), PageId(0))


class TestFileStorageCreateTable:
    def test_create_and_scan(self, file_store: FileStorage) -> None:
        file_store.create_table(TableName("t"), (_scd("a"), _scd("b")))
        file_store.insert_row(TableName("t"), (_t("x"), _t("y")))
        file_store.commit()
        rows = list(file_store.scan_rows(TableName("t")))
        assert len(rows) == 1

    def test_duplicate_table_raises(self, file_store: FileStorage) -> None:
        file_store.create_table(TableName("t"), (_scd("a"),))
        with pytest.raises(DuplicateTableError):
            file_store.create_table(TableName("t"), (_scd("b"),))

    def test_metadata_entry_too_large_raises(self, file_store: FileStorage) -> None:
        page = Page.empty(PAGE_TYPE_META)
        free_before = page.free_space()
        base_meta = TableMeta.serialize(TableName(""), (_scd("c"),), PageId(1))
        page.add_item(base_meta)
        per_item = free_before - page.free_space()
        itemid_size = per_item - len(base_meta)
        max_meta_bytes = free_before - itemid_size
        base_size = len(base_meta)
        name_len = max_meta_bytes - base_size + 1
        name = "t" * name_len

        with pytest.raises(RowTooLargeError):
            file_store.create_table(TableName(name), (_scd("c"),))
            file_store.commit()

    def test_get_columns(self, file_store: FileStorage) -> None:
        file_store.create_table(TableName("t"), (_scd("x"), _scd("y"), _scd("z")))
        cols = file_store.get_columns(TableName("t"))
        assert len(cols) == 3
        assert cols[0].name == "x"
        assert cols[1].name == "y"
        assert cols[2].name == "z"

    def test_get_columns_missing_table(self, file_store: FileStorage) -> None:
        with pytest.raises(TableNotFoundError):
            file_store.get_columns(TableName("missing"))

    def test_table_exists(self, file_store: FileStorage) -> None:
        assert not file_store.table_exists(TableName("t"))
        file_store.create_table(TableName("t"), (_scd("a"),))
        assert file_store.table_exists(TableName("t"))


class TestFileStorageInsertRow:
    def test_insert_and_scan(self, file_store: FileStorage) -> None:
        file_store.create_table(TableName("t"), (_scd("a"), _scd("b")))
        file_store.insert_row(TableName("t"), (_t("x"), _t("y")))
        file_store.commit()
        rows = list(file_store.scan_rows(TableName("t")))
        assert len(rows) == 1
        _, row = rows[0]
        assert row == (_t("x"), _t("y"))

    def test_insert_multiple_rows(self, file_store: FileStorage) -> None:
        file_store.create_table(TableName("t"), (_scd("a"),))
        file_store.insert_row(TableName("t"), (_t("1"),))
        file_store.insert_row(TableName("t"), (_t("2"),))
        file_store.insert_row(TableName("t"), (_t("3"),))
        file_store.commit()
        rows = list(file_store.scan_rows(TableName("t")))
        assert len(rows) == 3
        values = {r[1][0].value for r in rows}
        assert values == {"1", "2", "3"}

    def test_insert_missing_table(self, file_store: FileStorage) -> None:
        with pytest.raises(TableNotFoundError):
            file_store.insert_row(TableName("missing"), (_t("x"),))

    def test_insert_column_mismatch(self, file_store: FileStorage) -> None:
        file_store.create_table(TableName("t"), (_scd("a"), _scd("b")))
        with pytest.raises(ColumnMismatchError):
            file_store.insert_row(TableName("t"), (_t("x"),))

    def test_insert_row_too_large(self, file_store: FileStorage) -> None:
        file_store.create_table(TableName("t"), (_scd("val"),))
        page = Page.empty(PAGE_TYPE_DATA)
        free_before = page.free_space()
        empty_row = _StorageRowSerializer.serialize((_t(""),), (StorageColumnType.TEXT,))
        page.add_item(empty_row)
        per_item = free_before - page.free_space()
        itemid_size = per_item - len(empty_row)
        max_item_size = free_before - itemid_size
        payload_len = max_item_size - len(empty_row) + 1
        payload = "x" * payload_len
        with pytest.raises(RowTooLargeError):
            file_store.insert_row(TableName("t"), (_t(payload),))

    def test_insert_duplicate_values(self, file_store: FileStorage) -> None:
        file_store.create_table(TableName("t"), (_scd("a"),))
        file_store.insert_row(TableName("t"), (_t("x"),))
        file_store.insert_row(TableName("t"), (_t("x"),))
        file_store.commit()
        assert len(list(file_store.scan_rows(TableName("t")))) == 2


class TestFileStorageScanRows:
    def test_scan_empty_table(self, file_store: FileStorage) -> None:
        file_store.create_table(TableName("t"), (_scd("a"),))
        file_store.commit()
        assert list(file_store.scan_rows(TableName("t"))) == []

    def test_scan_missing_table(self, file_store: FileStorage) -> None:
        with pytest.raises(TableNotFoundError):
            list(file_store.scan_rows(TableName("missing")))


class TestFileStorageMarkUpdateCommit:
    def test_update_and_commit(self, file_store: FileStorage) -> None:
        file_store.create_table(TableName("t"), (_scd("a"),))
        file_store.insert_row(TableName("t"), (_t("x"),))
        file_store.commit()
        rid, _ = list(file_store.scan_rows(TableName("t")))[0]
        file_store.mark_update(TableName("t"), rid, (_t("z"),))
        file_store.commit()
        _, row = list(file_store.scan_rows(TableName("t")))[0]
        assert row == (_t("z"),)

    def test_update_not_visible_before_commit(self, file_store: FileStorage) -> None:
        file_store.create_table(TableName("t"), (_scd("a"),))
        file_store.insert_row(TableName("t"), (_t("x"),))
        file_store.commit()
        rid, _ = list(file_store.scan_rows(TableName("t")))[0]
        file_store.mark_update(TableName("t"), rid, (_t("z"),))
        _, row = list(file_store.scan_rows(TableName("t")))[0]
        assert row == (_t("x"),)

    def test_update_deleted_row_skipped(self, file_store: FileStorage) -> None:
        file_store.create_table(TableName("t"), (_scd("a"),))
        file_store.insert_row(TableName("t"), (_t("x"),))
        file_store.commit()
        rid, _ = list(file_store.scan_rows(TableName("t")))[0]
        file_store.mark_delete(TableName("t"), rid)
        file_store.mark_update(TableName("t"), rid, (_t("z"),))
        file_store.commit()
        assert len(list(file_store.scan_rows(TableName("t")))) == 0

    def test_update_column_mismatch(self, file_store: FileStorage) -> None:
        file_store.create_table(TableName("t"), (_scd("a"), _scd("b")))
        file_store.insert_row(TableName("t"), (_t("x"), _t("y")))
        file_store.commit()
        rid, _ = list(file_store.scan_rows(TableName("t")))[0]
        with pytest.raises(ColumnMismatchError):
            file_store.mark_update(TableName("t"), rid, (_t("z"),))

    def test_update_row_too_large_raises(self, file_store: FileStorage) -> None:
        file_store.create_table(TableName("t"), (_scd("val"),))
        file_store.insert_row(TableName("t"), (_t("x"),))
        file_store.commit()

        rid, _ = list(file_store.scan_rows(TableName("t")))[0]
        page = Page.empty(PAGE_TYPE_DATA)
        free_before = page.free_space()
        empty_row = _StorageRowSerializer.serialize((_t(""),), (StorageColumnType.TEXT,))
        page.add_item(empty_row)
        per_item = free_before - page.free_space()
        itemid_size = per_item - len(empty_row)
        max_item_size = free_before - itemid_size
        payload_len = max_item_size - len(empty_row) + 1
        payload = "x" * payload_len

        with pytest.raises(RowTooLargeError):
            file_store.mark_update(TableName("t"), rid, (_t(payload),))
            file_store.commit()


class TestFileStorageMarkDeleteCommit:
    def test_delete_and_commit(self, file_store: FileStorage) -> None:
        file_store.create_table(TableName("t"), (_scd("a"),))
        file_store.insert_row(TableName("t"), (_t("x"),))
        file_store.insert_row(TableName("t"), (_t("y"),))
        file_store.commit()
        rid = list(file_store.scan_rows(TableName("t")))[0][0]
        file_store.mark_delete(TableName("t"), rid)
        file_store.commit()
        assert len(list(file_store.scan_rows(TableName("t")))) == 1

    def test_delete_not_visible_before_commit(self, file_store: FileStorage) -> None:
        file_store.create_table(TableName("t"), (_scd("a"),))
        file_store.insert_row(TableName("t"), (_t("x"),))
        file_store.commit()
        rid, _ = list(file_store.scan_rows(TableName("t")))[0]
        file_store.mark_delete(TableName("t"), rid)
        assert len(list(file_store.scan_rows(TableName("t")))) == 1

    def test_delete_missing_table(self, file_store: FileStorage) -> None:
        with pytest.raises(TableNotFoundError):
            file_store.mark_delete(TableName("missing"), (PageId(0), SlotId(0)))


class TestFileStoragePersistence:
    def test_persistence_round_trip(self, tmp_path: Path) -> None:
        db_path = tmp_path / "test.db"
        store = FileStorage(db_path)
        store.create_table(TableName("users"), (_scd("name"), _scd("age")))
        store.insert_row(TableName("users"), (_t("alice"), _t("30")))
        store.insert_row(TableName("users"), (_t("bob"), _t("25")))
        store.commit()
        store.close()
        store2 = FileStorage(db_path)
        rows = list(store2.scan_rows(TableName("users")))
        assert len(rows) == 2
        values = {r[1][0].value for r in rows}
        assert values == {"alice", "bob"}

    def test_multiple_commits(self, tmp_path: Path) -> None:
        db_path = tmp_path / "test.db"
        store = FileStorage(db_path)
        store.create_table(TableName("t"), (_scd("a"),))
        store.insert_row(TableName("t"), (_t("1"),))
        store.commit()
        store.insert_row(TableName("t"), (_t("2"),))
        store.commit()
        store.close()
        store2 = FileStorage(db_path)
        rows = list(store2.scan_rows(TableName("t")))
        assert len(rows) == 2

    def test_update_persistence(self, tmp_path: Path) -> None:
        db_path = tmp_path / "test.db"
        store = FileStorage(db_path)
        store.create_table(TableName("t"), (_scd("a"),))
        store.insert_row(TableName("t"), (_t("x"),))
        store.commit()
        rid, _ = list(store.scan_rows(TableName("t")))[0]
        store.mark_update(TableName("t"), rid, (_t("y"),))
        store.commit()
        store.close()
        store2 = FileStorage(db_path)
        rows = list(store2.scan_rows(TableName("t")))
        assert len(rows) == 1
        assert rows[0][1] == (_t("y"),)

    def test_delete_persistence(self, tmp_path: Path) -> None:
        db_path = tmp_path / "test.db"
        store = FileStorage(db_path)
        store.create_table(TableName("t"), (_scd("a"),))
        store.insert_row(TableName("t"), (_t("1"),))
        store.insert_row(TableName("t"), (_t("2"),))
        store.commit()
        rid = list(store.scan_rows(TableName("t")))[0][0]
        store.mark_delete(TableName("t"), rid)
        store.commit()
        store.close()
        store2 = FileStorage(db_path)
        rows = list(store2.scan_rows(TableName("t")))
        assert len(rows) == 1

    def test_no_commit_no_persistence(self, tmp_path: Path) -> None:
        db_path = tmp_path / "test.db"
        store = FileStorage(db_path)
        store.create_table(TableName("t"), (_scd("a"),))
        store.insert_row(TableName("t"), (_t("x"),))
        store.close()
        store2 = FileStorage(db_path)
        assert not store2.table_exists(TableName("t"))

    def test_empty_commit_persistence(self, tmp_path: Path) -> None:
        db_path = tmp_path / "test.db"
        store = FileStorage(db_path)
        store.create_table(TableName("t"), (_scd("a"),))
        store.insert_row(TableName("t"), (_t("x"),))
        store.commit()
        store.commit()
        store.close()
        store2 = FileStorage(db_path)
        rows = list(store2.scan_rows(TableName("t")))
        assert len(rows) == 1

    def test_multi_table(self, tmp_path: Path) -> None:
        db_path = tmp_path / "test.db"
        store = FileStorage(db_path)
        store.create_table(TableName("users"), (_scd("name"),))
        store.create_table(TableName("posts"), (_scd("title"),))
        store.insert_row(TableName("users"), (_t("alice"),))
        store.insert_row(TableName("posts"), (_t("hello"),))
        store.commit()
        store.close()
        store2 = FileStorage(db_path)
        assert store2.table_exists(TableName("users"))
        assert store2.table_exists(TableName("posts"))
        assert len(list(store2.scan_rows(TableName("users")))) == 1
        assert len(list(store2.scan_rows(TableName("posts")))) == 1

    def test_unicode_values(self, tmp_path: Path) -> None:
        db_path = tmp_path / "test.db"
        store = FileStorage(db_path)
        store.create_table(TableName("t"), (_scd("val"),))
        store.insert_row(TableName("t"), (_t("日本語"),))
        store.commit()
        store.close()
        store2 = FileStorage(db_path)
        rows = list(store2.scan_rows(TableName("t")))
        assert len(rows) == 1
        assert rows[0][1] == (_t("日本語"),)

    def test_long_strings(self, tmp_path: Path) -> None:
        db_path = tmp_path / "test.db"
        store = FileStorage(db_path)
        store.create_table(TableName("t"), (_scd("val"),))
        store.insert_row(TableName("t"), (_t("x" * 500),))
        store.commit()
        store.close()
        store2 = FileStorage(db_path)
        rows = list(store2.scan_rows(TableName("t")))
        assert len(rows) == 1
        assert rows[0][1] == (_t("x" * 500),)

    def test_update_and_delete_different_rows(self, tmp_path: Path) -> None:
        db_path = tmp_path / "test.db"
        store = FileStorage(db_path)
        store.create_table(TableName("t"), (_scd("a"),))
        store.insert_row(TableName("t"), (_t("keep"),))
        store.insert_row(TableName("t"), (_t("delete"),))
        store.commit()
        rows = list(store.scan_rows(TableName("t")))
        store.mark_update(TableName("t"), rows[0][0], (_t("updated"),))
        store.mark_delete(TableName("t"), rows[1][0])
        store.commit()
        store.close()
        store2 = FileStorage(db_path)
        rows2 = list(store2.scan_rows(TableName("t")))
        assert len(rows2) == 1
        assert rows2[0][1] == (_t("updated"),)

    def test_corrupt_file_raises(self, tmp_path: Path) -> None:
        db_path = tmp_path / "test.db"
        db_path.write_bytes(b"corrupt data that is exactly page" + b"\x00" * (PAGE_SIZE - 30) + b"aligned!!")
        with pytest.raises(CorruptFileError):
            FileStorage(db_path)

    def test_metadata_cycle_raises(self, tmp_path: Path) -> None:
        db_path = tmp_path / "test.db"
        page0 = Page.empty(PAGE_TYPE_META)
        page1 = Page.empty(PAGE_TYPE_META)
        page2 = Page.empty(PAGE_TYPE_META)
        page0.header.next_page = PageId(1)
        page1.header.next_page = PageId(2)
        page2.header.next_page = PageId(1)
        db_path.write_bytes(page0.serialize() + page1.serialize() + page2.serialize())

        def _timeout(_signum: int, _frame: object) -> None:
            raise TimeoutError("metadata cycle did not terminate")

        old_handler = signal.signal(signal.SIGALRM, _timeout)
        signal.alarm(1)
        try:
            with pytest.raises(CorruptFileError):
                FileStorage(db_path)
        except TimeoutError:
            pytest.fail("FileStorage hangs on metadata page cycles")
        finally:
            signal.alarm(0)
            signal.signal(signal.SIGALRM, old_handler)

    def test_metadata_page_overflow_persists(self, tmp_path: Path) -> None:
        db_path = tmp_path / "test.db"
        store = FileStorage(db_path)
        max_tables = _tables_per_meta_page("t0000", (_scd("c"),))
        total_tables = max_tables + 2
        for i in range(total_tables):
            store.create_table(TableName(f"t{i:04d}"), (_scd("c"),))
        store.insert_row(TableName("t0000"), (_t("first"),))
        store.insert_row(TableName(f"t{total_tables - 1:04d}"), (_t("last"),))
        store.commit()
        store.close()
        store2 = FileStorage(db_path)
        for i in range(total_tables):
            assert store2.table_exists(TableName(f"t{i:04d}"))
        assert list(store2.scan_rows(TableName("t0000")))[0][1] == (_t("first"),)
        assert list(store2.scan_rows(TableName(f"t{total_tables - 1:04d}")))[0][1] == (_t("last"),)

    def test_metadata_page_growth_after_reload(self, tmp_path: Path) -> None:
        db_path = tmp_path / "test.db"
        store = FileStorage(db_path)
        max_tables = _tables_per_meta_page("t0000", (_scd("c"),))
        for i in range(max_tables):
            store.create_table(TableName(f"t{i:04d}"), (_scd("c"),))
        store.commit()
        store.close()

        store2 = FileStorage(db_path)
        store2.create_table(TableName(f"t{max_tables:04d}"), (_scd("c"),))
        store2.insert_row(TableName(f"t{max_tables:04d}"), (_t("grown"),))
        store2.commit()
        store2.close()

        store3 = FileStorage(db_path)
        assert store3.table_exists(TableName(f"t{max_tables:04d}"))
        assert list(store3.scan_rows(TableName(f"t{max_tables:04d}")))[0][1] == (_t("grown"),)

    def test_non_continuous_page_allocation(self, tmp_path: Path) -> None:
        db_path = tmp_path / "test.db"
        store = FileStorage(db_path)

        payload = "x" * (PAGE_SIZE // 4)
        rows_per_page = _rows_per_page(payload)

        store.create_table(TableName("table_a"), (_scd("col"),))
        for _ in range(rows_per_page):
            store.insert_row(TableName("table_a"), (_t(payload),))
        store.commit()

        store.create_table(TableName("table_b"), (_scd("col"),))
        store.insert_row(TableName("table_b"), (_t("b_row"),))
        store.commit()

        store.insert_row(TableName("table_a"), (_t(payload),))
        store.commit()

        rows_a = list(store.scan_rows(TableName("table_a")))
        rows_b = list(store.scan_rows(TableName("table_b")))

        assert (
            len(rows_a) == rows_per_page + 1
        ), f"Expected {rows_per_page + 1} rows for table_a, got {len(rows_a)}"
        assert len(rows_b) == 1


class TestFileStorageCompaction:
    def test_compaction_delete_all(self, tmp_path: Path) -> None:
        db_path = tmp_path / "test.db"
        store = FileStorage(db_path)
        store.create_table(TableName("t"), (_scd("val"),))
        payload = "x" * (PAGE_SIZE // 4)
        rows_per_page = _rows_per_page(payload)
        total_rows = rows_per_page * 3 + 1
        for _ in range(total_rows):
            store.insert_row(TableName("t"), (_t(payload),))
        store.commit()

        rows = list(store.scan_rows(TableName("t")))
        for rid, _ in rows:
            store.mark_delete(TableName("t"), rid)
        store.commit()

        assert list(store.scan_rows(TableName("t"))) == []
        store.vacuum()
        assert db_path.stat().st_size == PAGE_SIZE * 2

    def test_compaction_complex_deletion_pattern(self, tmp_path: Path) -> None:
        db_path = tmp_path / "test.db"
        store = FileStorage(db_path)
        store.create_table(TableName("t"), (_scd("val"),))
        payload = "x" * (PAGE_SIZE // 5)
        rows_per_page = _rows_per_page(payload)
        total_rows = rows_per_page * 4 + 2
        for _ in range(total_rows):
            store.insert_row(TableName("t"), (_t(payload),))
        store.commit()

        rows = list(store.scan_rows(TableName("t")))
        keep_indices: set[int] = set()
        for i in range(total_rows):
            if i % 2 == 0 and i % 3 == 0:
                keep_indices.add(i)
            if i % 5 == 1:
                keep_indices.add(i)
        for i, (rid, _) in enumerate(rows):
            if i not in keep_indices:
                store.mark_delete(TableName("t"), rid)
        store.commit()

        assert len(list(store.scan_rows(TableName("t")))) == len(keep_indices)
        store.vacuum()
        expected_pages = (len(keep_indices) + rows_per_page - 1) // rows_per_page
        assert db_path.stat().st_size == PAGE_SIZE * (1 + expected_pages)

    def test_compaction_multiple_tables_complex_patterns(self, tmp_path: Path) -> None:
        db_path = tmp_path / "test.db"
        store = FileStorage(db_path)

        payload_a = "a" * (PAGE_SIZE // 6)
        payload_b = "b" * (PAGE_SIZE // 7)
        payload_c = "c" * (PAGE_SIZE // 8)
        rows_per_page_a = _rows_per_page(payload_a)
        rows_per_page_b = _rows_per_page(payload_b)
        rows_per_page_c = _rows_per_page(payload_c)

        store.create_table(TableName("a"), (_scd("val"),))
        for _ in range(rows_per_page_a * 3 + 1):
            store.insert_row(TableName("a"), (_t(payload_a),))
        store.create_table(TableName("b"), (_scd("val"),))
        for _ in range(rows_per_page_b * 2 + 2):
            store.insert_row(TableName("b"), (_t(payload_b),))
        store.create_table(TableName("c"), (_scd("val"),))
        for _ in range(rows_per_page_c * 4 + 3):
            store.insert_row(TableName("c"), (_t(payload_c),))
        store.commit()

        rows_a = list(store.scan_rows(TableName("a")))
        rows_b = list(store.scan_rows(TableName("b")))
        rows_c = list(store.scan_rows(TableName("c")))

        keep_a = {i for i in range(len(rows_a)) if i % 3 == 0}
        keep_b = {i for i in range(len(rows_b)) if i % 2 == 1 or i % 5 == 0}
        keep_c = {i for i in range(len(rows_c)) if i % 4 == 0 or i % 7 == 3}

        for i, (rid, _) in enumerate(rows_a):
            if i not in keep_a:
                store.mark_delete(TableName("a"), rid)
        for i, (rid, _) in enumerate(rows_b):
            if i not in keep_b:
                store.mark_delete(TableName("b"), rid)
        for i, (rid, _) in enumerate(rows_c):
            if i not in keep_c:
                store.mark_delete(TableName("c"), rid)
        store.commit()
        assert len(list(store.scan_rows(TableName("a")))) == len(keep_a)
        assert len(list(store.scan_rows(TableName("b")))) == len(keep_b)
        assert len(list(store.scan_rows(TableName("c")))) == len(keep_c)
        store.vacuum()

        expected_pages_a = (len(keep_a) + rows_per_page_a - 1) // rows_per_page_a
        expected_pages_b = (len(keep_b) + rows_per_page_b - 1) // rows_per_page_b
        expected_pages_c = (len(keep_c) + rows_per_page_c - 1) // rows_per_page_c
        assert db_path.stat().st_size == PAGE_SIZE * (
            1 + expected_pages_a + expected_pages_b + expected_pages_c
        )

    def test_compaction_interleaved_meta_and_data_pages(self, tmp_path: Path) -> None:
        db_path = tmp_path / "test.db"
        store = FileStorage(db_path)

        data_payload = "d" * (PAGE_SIZE // 5)
        rows_per_page = _rows_per_page(data_payload)

        store.create_table(TableName("early_data"), (_scd("val"),))
        for _ in range(rows_per_page * 3):
            store.insert_row(TableName("early_data"), (_t(data_payload),))

        max_tables = _tables_per_meta_page("t0000", (_scd("c"),))
        total_tables = max_tables + 2
        for i in range(total_tables):
            store.create_table(TableName(f"t{i:04d}"), (_scd("c"),))

        store.create_table(TableName("late_data"), (_scd("val"),))
        for _ in range(rows_per_page * 2):
            store.insert_row(TableName("late_data"), (_t(data_payload),))

        for i in range(total_tables):
            store.insert_row(TableName(f"t{i:04d}"), (_t(f"val{i}"),))
        store.commit()

        for i, (rid, _) in enumerate(store.scan_rows(TableName("early_data"))):
            if i % 3 != 0:
                store.mark_delete(TableName("early_data"), rid)
        for i, (rid, _) in enumerate(store.scan_rows(TableName("late_data"))):
            if i % 4 != 0:
                store.mark_delete(TableName("late_data"), rid)
        for i in range(total_tables):
            if i % 2 == 0:
                rid, _ = list(store.scan_rows(TableName(f"t{i:04d}")))[0]
                store.mark_delete(TableName(f"t{i:04d}"), rid)
        store.commit()

        early_count = len(list(store.scan_rows(TableName("early_data"))))
        late_count = len(list(store.scan_rows(TableName("late_data"))))
        size_before = db_path.stat().st_size
        store.vacuum()
        store.close()

        store2 = FileStorage(db_path)
        assert len(list(store2.scan_rows(TableName("early_data")))) == early_count
        assert len(list(store2.scan_rows(TableName("late_data")))) == late_count
        for i in range(total_tables):
            name = TableName(f"t{i:04d}")
            assert store2.table_exists(name)
            rows = list(store2.scan_rows(name))
            if i % 2 == 0:
                assert rows == []
            else:
                assert rows[0][1] == (_t(f"val{i}"),)

        per_data_page = _rows_per_page(data_payload)
        expected_early = (early_count + per_data_page - 1) // per_data_page
        expected_late = (late_count + per_data_page - 1) // per_data_page
        expected_data_pages_for_meta = sum(
            1 for i in range(total_tables) if i % 2 != 0
        )
        per_empty_meta = _tables_per_meta_page("t0000", (_scd("c"),))
        num_meta_pages = (total_tables + per_empty_meta - 1) // per_empty_meta
        surviving_tables = sum(1 for i in range(total_tables) if i % 2 != 0)
        empty_table_pages = total_tables - surviving_tables
        expected_size = PAGE_SIZE * (
            num_meta_pages
            + expected_early
            + expected_late
            + expected_data_pages_for_meta
            + empty_table_pages
        )
        assert db_path.stat().st_size == expected_size
        assert db_path.stat().st_size < size_before

    def test_compaction_multi_meta_pages(self, tmp_path: Path) -> None:
        db_path = tmp_path / "test.db"
        store = FileStorage(db_path)
        max_tables = _tables_per_meta_page("t0000", (_scd("c"),))
        total_tables = max_tables + 3
        for i in range(total_tables):
            name = TableName(f"t{i:04d}")
            store.create_table(name, (_scd("c"),))
            store.insert_row(name, (_t(f"v{i}"),))
        store.commit()

        for i in range(0, total_tables, 2):
            name = TableName(f"t{i:04d}")
            rid, _ = list(store.scan_rows(name))[0]
            store.mark_delete(name, rid)
        store.commit()
        store.vacuum()
        store.close()

        store2 = FileStorage(db_path)
        for i in range(total_tables):
            name = TableName(f"t{i:04d}")
            assert store2.table_exists(name)
            rows = list(store2.scan_rows(name))
            if i % 2 == 0:
                assert rows == []
            else:
                assert rows[0][1] == (_t(f"v{i}"),)
