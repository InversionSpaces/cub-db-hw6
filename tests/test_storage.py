import signal
import struct

import pytest
from pathlib import Path

from dbms.errors import (
    ColumnMismatchError,
    CorruptFileError,
    DuplicateTableError,
    RowTooLargeError,
    TableNotFoundError,
)
from dbms.storage import (
    FileStorage,
    Page,
    PageId,
    SlotId,
    StorageRow,
    TableMeta,
    PAGE_SIZE,
    PAGE_TYPE_DATA,
    PAGE_TYPE_META,
)
from dbms.in_memory_storage import InMemoryStorage


@pytest.fixture
def store() -> InMemoryStorage:
    return InMemoryStorage()


@pytest.fixture
def file_store(tmp_path: Path) -> FileStorage:
    return FileStorage(tmp_path / "test.db")


def _rows_per_page(payload: str) -> int:
    row_bytes = StorageRow.serialize((payload,))
    page = Page.empty(PAGE_TYPE_DATA)
    free_before = page.free_space()
    page.add_item(row_bytes)
    per_item = free_before - page.free_space()
    return free_before // per_item


def _tables_per_meta_page(name: str, columns: tuple[str, ...]) -> int:
    meta_bytes = TableMeta.serialize(name, columns, 1)
    page = Page.empty(PAGE_TYPE_META)
    free_before = page.free_space()
    page.add_item(meta_bytes)
    per_item = free_before - page.free_space()
    return free_before // per_item


class TestCreateTable:
    def test_create_and_scan(self, store: InMemoryStorage) -> None:
        store.create_table("t", ("a", "b"))
        store.insert_row("t", ("x", "y"))
        rows = list(store.scan_rows("t"))
        assert len(rows) == 1

    def test_duplicate_table_raises(self, store: InMemoryStorage) -> None:
        store.create_table("t", ("a",))
        with pytest.raises(DuplicateTableError):
            store.create_table("t", ("b",))

    def test_get_columns(self, store: InMemoryStorage) -> None:
        store.create_table("t", ("x", "y", "z"))
        assert store.get_columns("t") == ("x", "y", "z")

    def test_get_columns_missing_table(self, store: InMemoryStorage) -> None:
        with pytest.raises(TableNotFoundError):
            store.get_columns("missing")

    def test_table_exists(self, store: InMemoryStorage) -> None:
        assert not store.table_exists("t")
        store.create_table("t", ("a",))
        assert store.table_exists("t")


class TestInsertRow:
    def test_insert_and_scan(self, store: InMemoryStorage) -> None:
        store.create_table("t", ("a", "b"))
        store.insert_row("t", ("x", "y"))
        rows = list(store.scan_rows("t"))
        assert len(rows) == 1
        _, row = rows[0]
        assert row == ("x", "y")

    def test_insert_multiple_rows(self, store: InMemoryStorage) -> None:
        store.create_table("t", ("a",))
        store.insert_row("t", ("1",))
        store.insert_row("t", ("2",))
        store.insert_row("t", ("3",))
        rows = list(store.scan_rows("t"))
        assert len(rows) == 3
        values = {r[1][0] for r in rows}
        assert values == {"1", "2", "3"}

    def test_insert_missing_table(self, store: InMemoryStorage) -> None:
        with pytest.raises(TableNotFoundError):
            store.insert_row("missing", ("x",))

    def test_insert_column_mismatch(self, store: InMemoryStorage) -> None:
        store.create_table("t", ("a", "b"))
        with pytest.raises(ColumnMismatchError):
            store.insert_row("t", ("x",))

    def test_insert_duplicate_values(self, store: InMemoryStorage) -> None:
        store.create_table("t", ("a",))
        store.insert_row("t", ("x",))
        store.insert_row("t", ("x",))
        assert len(list(store.scan_rows("t"))) == 2

    def test_insert_after_delete(self, store: InMemoryStorage) -> None:
        store.create_table("t", ("a",))
        store.insert_row("t", ("x",))
        rid, _ = list(store.scan_rows("t"))[0]
        store.mark_delete("t", rid)
        store.commit()
        store.insert_row("t", ("y",))
        rows = list(store.scan_rows("t"))
        assert len(rows) == 1
        assert rows[0][1] == ("y",)


class TestScanRows:
    def test_scan_empty_table(self, store: InMemoryStorage) -> None:
        store.create_table("t", ("a",))
        assert list(store.scan_rows("t")) == []

    def test_scan_missing_table(self, store: InMemoryStorage) -> None:
        with pytest.raises(TableNotFoundError):
            list(store.scan_rows("missing"))


class TestMarkUpdateCommit:
    def test_update_and_commit(self, store: InMemoryStorage) -> None:
        store.create_table("t", ("a",))
        store.insert_row("t", ("x",))
        rid, _ = list(store.scan_rows("t"))[0]
        store.mark_update("t", rid, ("z",))
        _, row = list(store.scan_rows("t"))[0]
        assert row == ("x",)
        store.commit()
        _, row = list(store.scan_rows("t"))[0]
        assert row == ("z",)

    def test_update_not_visible_before_commit(self, store: InMemoryStorage) -> None:
        store.create_table("t", ("a",))
        store.insert_row("t", ("x",))
        rid, _ = list(store.scan_rows("t"))[0]
        store.mark_update("t", rid, ("z",))
        _, row = list(store.scan_rows("t"))[0]
        assert row == ("x",)

    def test_multiple_updates_last_write_wins(self, store: InMemoryStorage) -> None:
        store.create_table("t", ("a",))
        store.insert_row("t", ("x",))
        rid, _ = list(store.scan_rows("t"))[0]
        store.mark_update("t", rid, ("y",))
        store.mark_update("t", rid, ("z",))
        store.commit()
        _, row = list(store.scan_rows("t"))[0]
        assert row == ("z",)

    def test_update_multiple_rows(self, store: InMemoryStorage) -> None:
        store.create_table("t", ("a",))
        store.insert_row("t", ("1",))
        store.insert_row("t", ("2",))
        rows = list(store.scan_rows("t"))
        store.mark_update("t", rows[0][0], ("x",))
        store.mark_update("t", rows[1][0], ("y",))
        store.commit()
        values = {r[1][0] for r in store.scan_rows("t")}
        assert values == {"x", "y"}

    def test_update_deleted_row_skipped(self, store: InMemoryStorage) -> None:
        store.create_table("t", ("a",))
        store.insert_row("t", ("x",))
        rid, _ = list(store.scan_rows("t"))[0]
        store.mark_delete("t", rid)
        store.mark_update("t", rid, ("z",))
        store.commit()
        assert len(list(store.scan_rows("t"))) == 0

    def test_update_column_mismatch(self, store: InMemoryStorage) -> None:
        store.create_table("t", ("a", "b"))
        store.insert_row("t", ("x", "y"))
        rid, _ = list(store.scan_rows("t"))[0]
        with pytest.raises(ColumnMismatchError):
            store.mark_update("t", rid, ("z",))

    def test_update_missing_table(self, store: InMemoryStorage) -> None:
        with pytest.raises(TableNotFoundError):
            store.mark_update("missing", (PageId(0), SlotId(0)), ("z",))


class TestMarkDeleteCommit:
    def test_delete_and_commit(self, store: InMemoryStorage) -> None:
        store.create_table("t", ("a",))
        store.insert_row("t", ("x",))
        store.insert_row("t", ("y",))
        rid = list(store.scan_rows("t"))[0][0]
        store.mark_delete("t", rid)
        assert len(list(store.scan_rows("t"))) == 2
        store.commit()
        assert len(list(store.scan_rows("t"))) == 1

    def test_delete_multiple_rows(self, store: InMemoryStorage) -> None:
        store.create_table("t", ("a",))
        store.insert_row("t", ("1",))
        store.insert_row("t", ("2",))
        store.insert_row("t", ("3",))
        rows = list(store.scan_rows("t"))
        store.mark_delete("t", rows[0][0])
        store.mark_delete("t", rows[1][0])
        store.commit()
        assert len(list(store.scan_rows("t"))) == 1

    def test_delete_not_visible_before_commit(self, store: InMemoryStorage) -> None:
        store.create_table("t", ("a",))
        store.insert_row("t", ("x",))
        rid, _ = list(store.scan_rows("t"))[0]
        store.mark_delete("t", rid)
        assert len(list(store.scan_rows("t"))) == 1

    def test_delete_missing_table(self, store: InMemoryStorage) -> None:
        with pytest.raises(TableNotFoundError):
            store.mark_delete("missing", (PageId(0), SlotId(0)))


class TestCommitWithUpdatesAndDeletes:
    def test_update_and_delete_different_rows(self, store: InMemoryStorage) -> None:
        store.create_table("t", ("a",))
        store.insert_row("t", ("keep",))
        store.insert_row("t", ("delete",))
        rows = list(store.scan_rows("t"))
        store.mark_update("t", rows[0][0], ("updated",))
        store.mark_delete("t", rows[1][0])
        store.commit()
        rows = list(store.scan_rows("t"))
        assert len(rows) == 1
        assert rows[0][1] == ("updated",)

    def test_commit_clears_pending(self, store: InMemoryStorage) -> None:
        store.create_table("t", ("a",))
        store.insert_row("t", ("x",))
        rid, _ = list(store.scan_rows("t"))[0]
        store.mark_update("t", rid, ("y",))
        store.commit()
        store.mark_delete("t", rid)
        store.commit()
        assert len(list(store.scan_rows("t"))) == 0

    def test_empty_commit_is_noop(self, store: InMemoryStorage) -> None:
        store.create_table("t", ("a",))
        store.insert_row("t", ("x",))
        store.commit()
        assert len(list(store.scan_rows("t"))) == 1


class TestRowSerialization:
    def test_roundtrip_single_col(self) -> None:
        row = ("hello",)
        assert StorageRow.deserialize(StorageRow.serialize(row)) == row

    def test_roundtrip_multi_col(self) -> None:
        row = ("abc", "def", "ghi")
        assert StorageRow.deserialize(StorageRow.serialize(row)) == row

    def test_roundtrip_empty_string(self) -> None:
        row = ("",)
        assert StorageRow.deserialize(StorageRow.serialize(row)) == row

    def test_roundtrip_unicode(self) -> None:
        row = ("日本語", "emoji🎉")
        assert StorageRow.deserialize(StorageRow.serialize(row)) == row

    def test_roundtrip_long_string(self) -> None:
        row = ("x" * 500,)
        assert StorageRow.deserialize(StorageRow.serialize(row)) == row


class TestTableDefSerialization:
    def test_roundtrip_simple(self) -> None:
        data = TableMeta.serialize("users", ("name", "age"), 1)
        meta = TableMeta.deserialize(data)
        assert meta.name == "users"
        assert meta.columns == ("name", "age")
        assert meta.head_data_page == 1

    def test_roundtrip_single_col(self) -> None:
        data = TableMeta.serialize("t", ("a",), 0)
        meta = TableMeta.deserialize(data)
        assert meta.name == "t"
        assert meta.columns == ("a",)
        assert meta.head_data_page == 0

    def test_roundtrip_unicode_name(self) -> None:
        data = TableMeta.serialize("テーブル", ("列1", "列2"), 5)
        meta = TableMeta.deserialize(data)
        assert meta.name == "テーブル"
        assert meta.columns == ("列1", "列2")
        assert meta.head_data_page == 5


class TestPageRoundtrip:
    def test_empty_page_roundtrip(self) -> None:
        page = Page.empty(PAGE_TYPE_DATA)
        data = page.serialize()
        assert len(data) == PAGE_SIZE
        restored = Page.deserialize(data, 0)
        assert restored.header.page_type == PAGE_TYPE_DATA
        assert restored.header.num_items == 0
        assert len(restored.items) == 0

    def test_page_with_items_roundtrip(self) -> None:
        page = Page.empty(PAGE_TYPE_DATA)
        row_bytes = StorageRow.serialize(("hello", "world"))
        page.add_item(row_bytes)
        row_bytes2 = StorageRow.serialize(("foo",))
        page.add_item(row_bytes2)
        data = page.serialize()
        restored = Page.deserialize(data, 0)
        assert restored.header.num_items == 2
        assert len(restored.items) == 2
        assert StorageRow.deserialize(restored.items[0]) == ("hello", "world")
        assert StorageRow.deserialize(restored.items[1]) == ("foo",)

    def test_metadata_page_roundtrip(self) -> None:
        page = Page.empty(PAGE_TYPE_META)
        item = TableMeta.serialize("users", ("name", "age"), 1)
        page.add_item(item)
        data = page.serialize()
        restored = Page.deserialize(data, 0)
        assert restored.header.page_type == PAGE_TYPE_META
        assert len(restored.items) == 1
        meta = TableMeta.deserialize(restored.items[0])
        assert meta.name == "users"
        assert meta.columns == ("name", "age")
        assert meta.head_data_page == 1

    def test_free_space_tracking(self) -> None:
        page = Page.empty(PAGE_TYPE_DATA)
        assert page.free_space() == PAGE_SIZE - 12
        row_bytes = StorageRow.serialize(("a",))
        page.add_item(row_bytes)
        assert page.free_space() == PAGE_SIZE - 12 - 4 - len(row_bytes)

    def test_corrupt_page_raises(self) -> None:
        page = Page.empty(PAGE_TYPE_DATA)
        data = bytearray(page.serialize())
        struct.pack_into("<H", data, 4, 3000)
        struct.pack_into("<H", data, 6, 2000)
        with pytest.raises(CorruptFileError):
            Page.deserialize(bytes(data), 0)


class TestFileStorageCreateTable:
    def test_create_and_scan(self, file_store: FileStorage) -> None:
        file_store.create_table("t", ("a", "b"))
        file_store.insert_row("t", ("x", "y"))
        rows = list(file_store.scan_rows("t"))
        assert len(rows) == 1

    def test_duplicate_table_raises(self, file_store: FileStorage) -> None:
        file_store.create_table("t", ("a",))
        with pytest.raises(DuplicateTableError):
            file_store.create_table("t", ("b",))

    def test_metadata_entry_too_large_raises(self, file_store: FileStorage) -> None:
        page = Page.empty(PAGE_TYPE_META)
        free_before = page.free_space()
        base_meta = TableMeta.serialize("", ("c",), 1)
        page.add_item(base_meta)
        per_item = free_before - page.free_space()
        itemid_size = per_item - len(base_meta)
        max_meta_bytes = free_before - itemid_size
        base_size = len(base_meta)
        name_len = max_meta_bytes - base_size + 1
        name = "t" * name_len

        with pytest.raises(RowTooLargeError):
            file_store.create_table(name, ("c",))
            file_store.commit()

    def test_get_columns(self, file_store: FileStorage) -> None:
        file_store.create_table("t", ("x", "y", "z"))
        assert file_store.get_columns("t") == ("x", "y", "z")

    def test_get_columns_missing_table(self, file_store: FileStorage) -> None:
        with pytest.raises(TableNotFoundError):
            file_store.get_columns("missing")

    def test_table_exists(self, file_store: FileStorage) -> None:
        assert not file_store.table_exists("t")
        file_store.create_table("t", ("a",))
        assert file_store.table_exists("t")


class TestFileStorageInsertRow:
    def test_insert_and_scan(self, file_store: FileStorage) -> None:
        file_store.create_table("t", ("a", "b"))
        file_store.insert_row("t", ("x", "y"))
        file_store.commit()
        rows = list(file_store.scan_rows("t"))
        assert len(rows) == 1
        _, row = rows[0]
        assert row == ("x", "y")

    def test_insert_multiple_rows(self, file_store: FileStorage) -> None:
        file_store.create_table("t", ("a",))
        file_store.insert_row("t", ("1",))
        file_store.insert_row("t", ("2",))
        file_store.insert_row("t", ("3",))
        file_store.commit()
        rows = list(file_store.scan_rows("t"))
        assert len(rows) == 3
        values = {r[1][0] for r in rows}
        assert values == {"1", "2", "3"}

    def test_insert_missing_table(self, file_store: FileStorage) -> None:
        with pytest.raises(TableNotFoundError):
            file_store.insert_row("missing", ("x",))

    def test_insert_column_mismatch(self, file_store: FileStorage) -> None:
        file_store.create_table("t", ("a", "b"))
        with pytest.raises(ColumnMismatchError):
            file_store.insert_row("t", ("x",))

    def test_insert_row_too_large(self, file_store: FileStorage) -> None:
        file_store.create_table("t", ("val",))
        page = Page.empty(PAGE_TYPE_DATA)
        free_before = page.free_space()
        empty_row = StorageRow.serialize(("",))
        page.add_item(empty_row)
        per_item = free_before - page.free_space()
        itemid_size = per_item - len(empty_row)
        max_item_size = free_before - itemid_size
        payload_len = max_item_size - len(empty_row) + 1
        payload = "x" * payload_len
        with pytest.raises(RowTooLargeError):
            file_store.insert_row("t", (payload,))

    def test_insert_duplicate_values(self, file_store: FileStorage) -> None:
        file_store.create_table("t", ("a",))
        file_store.insert_row("t", ("x",))
        file_store.insert_row("t", ("x",))
        file_store.commit()
        assert len(list(file_store.scan_rows("t"))) == 2


class TestFileStorageScanRows:
    def test_scan_empty_table(self, file_store: FileStorage) -> None:
        file_store.create_table("t", ("a",))
        assert list(file_store.scan_rows("t")) == []

    def test_scan_missing_table(self, file_store: FileStorage) -> None:
        with pytest.raises(TableNotFoundError):
            list(file_store.scan_rows("missing"))


class TestFileStorageMarkUpdateCommit:
    def test_update_and_commit(self, file_store: FileStorage) -> None:
        file_store.create_table("t", ("a",))
        file_store.insert_row("t", ("x",))
        file_store.commit()
        rid, _ = list(file_store.scan_rows("t"))[0]
        file_store.mark_update("t", rid, ("z",))
        file_store.commit()
        _, row = list(file_store.scan_rows("t"))[0]
        assert row == ("z",)

    def test_update_not_visible_before_commit(self, file_store: FileStorage) -> None:
        file_store.create_table("t", ("a",))
        file_store.insert_row("t", ("x",))
        file_store.commit()
        rid, _ = list(file_store.scan_rows("t"))[0]
        file_store.mark_update("t", rid, ("z",))
        _, row = list(file_store.scan_rows("t"))[0]
        assert row == ("x",)

    def test_update_deleted_row_skipped(self, file_store: FileStorage) -> None:
        file_store.create_table("t", ("a",))
        file_store.insert_row("t", ("x",))
        file_store.commit()
        rid, _ = list(file_store.scan_rows("t"))[0]
        file_store.mark_delete("t", rid)
        file_store.mark_update("t", rid, ("z",))
        file_store.commit()
        assert len(list(file_store.scan_rows("t"))) == 0

    def test_update_column_mismatch(self, file_store: FileStorage) -> None:
        file_store.create_table("t", ("a", "b"))
        file_store.insert_row("t", ("x", "y"))
        file_store.commit()
        rid, _ = list(file_store.scan_rows("t"))[0]
        with pytest.raises(ColumnMismatchError):
            file_store.mark_update("t", rid, ("z",))

    def test_update_row_too_large_raises(self, file_store: FileStorage) -> None:
        file_store.create_table("t", ("val",))
        file_store.insert_row("t", ("x",))
        file_store.commit()

        rid, _ = list(file_store.scan_rows("t"))[0]
        page = Page.empty(PAGE_TYPE_DATA)
        free_before = page.free_space()
        empty_row = StorageRow.serialize(("",))
        page.add_item(empty_row)
        per_item = free_before - page.free_space()
        itemid_size = per_item - len(empty_row)
        max_item_size = free_before - itemid_size
        payload_len = max_item_size - len(empty_row) + 1
        payload = "x" * payload_len

        with pytest.raises(RowTooLargeError):
            file_store.mark_update("t", rid, (payload,))
            file_store.commit()

class TestFileStorageMarkDeleteCommit:
    def test_delete_and_commit(self, file_store: FileStorage) -> None:
        file_store.create_table("t", ("a",))
        file_store.insert_row("t", ("x",))
        file_store.insert_row("t", ("y",))
        file_store.commit()
        rid = list(file_store.scan_rows("t"))[0][0]
        file_store.mark_delete("t", rid)
        file_store.commit()
        assert len(list(file_store.scan_rows("t"))) == 1

    def test_delete_not_visible_before_commit(self, file_store: FileStorage) -> None:
        file_store.create_table("t", ("a",))
        file_store.insert_row("t", ("x",))
        file_store.commit()
        rid, _ = list(file_store.scan_rows("t"))[0]
        file_store.mark_delete("t", rid)
        assert len(list(file_store.scan_rows("t"))) == 1

    def test_delete_missing_table(self, file_store: FileStorage) -> None:
        with pytest.raises(TableNotFoundError):
            file_store.mark_delete("missing", (PageId(0), SlotId(0)))


class TestFileStoragePersistence:
    def test_persistence_round_trip(self, tmp_path: Path) -> None:
        db_path = tmp_path / "test.db"
        store = FileStorage(db_path)
        store.create_table("users", ("name", "age"))
        store.insert_row("users", ("alice", "30"))
        store.insert_row("users", ("bob", "25"))
        store.commit()
        store.close()
        store2 = FileStorage(db_path)
        rows = list(store2.scan_rows("users"))
        assert len(rows) == 2
        values = {r[1][0] for r in rows}
        assert values == {"alice", "bob"}

    def test_multiple_commits(self, tmp_path: Path) -> None:
        db_path = tmp_path / "test.db"
        store = FileStorage(db_path)
        store.create_table("t", ("a",))
        store.insert_row("t", ("1",))
        store.commit()
        store.insert_row("t", ("2",))
        store.commit()
        store.close()
        store2 = FileStorage(db_path)
        rows = list(store2.scan_rows("t"))
        assert len(rows) == 2

    def test_update_persistence(self, tmp_path: Path) -> None:
        db_path = tmp_path / "test.db"
        store = FileStorage(db_path)
        store.create_table("t", ("a",))
        store.insert_row("t", ("x",))
        store.commit()
        rid, _ = list(store.scan_rows("t"))[0]
        store.mark_update("t", rid, ("y",))
        store.commit()
        store.close()
        store2 = FileStorage(db_path)
        rows = list(store2.scan_rows("t"))
        assert len(rows) == 1
        assert rows[0][1] == ("y",)

    def test_delete_persistence(self, tmp_path: Path) -> None:
        db_path = tmp_path / "test.db"
        store = FileStorage(db_path)
        store.create_table("t", ("a",))
        store.insert_row("t", ("1",))
        store.insert_row("t", ("2",))
        store.commit()
        rid = list(store.scan_rows("t"))[0][0]
        store.mark_delete("t", rid)
        store.commit()
        store.close()
        store2 = FileStorage(db_path)
        rows = list(store2.scan_rows("t"))
        assert len(rows) == 1

    def test_no_commit_no_persistence(self, tmp_path: Path) -> None:
        db_path = tmp_path / "test.db"
        store = FileStorage(db_path)
        store.create_table("t", ("a",))
        store.insert_row("t", ("x",))
        store.close()
        store2 = FileStorage(db_path)
        assert not store2.table_exists("t")

    def test_empty_commit_persistence(self, tmp_path: Path) -> None:
        db_path = tmp_path / "test.db"
        store = FileStorage(db_path)
        store.create_table("t", ("a",))
        store.insert_row("t", ("x",))
        store.commit()
        store.commit()
        store.close()
        store2 = FileStorage(db_path)
        rows = list(store2.scan_rows("t"))
        assert len(rows) == 1

    def test_multi_table(self, tmp_path: Path) -> None:
        db_path = tmp_path / "test.db"
        store = FileStorage(db_path)
        store.create_table("users", ("name",))
        store.create_table("posts", ("title",))
        store.insert_row("users", ("alice",))
        store.insert_row("posts", ("hello",))
        store.commit()
        store.close()
        store2 = FileStorage(db_path)
        assert store2.table_exists("users")
        assert store2.table_exists("posts")
        assert len(list(store2.scan_rows("users"))) == 1
        assert len(list(store2.scan_rows("posts"))) == 1

    def test_unicode_values(self, tmp_path: Path) -> None:
        db_path = tmp_path / "test.db"
        store = FileStorage(db_path)
        store.create_table("t", ("val",))
        store.insert_row("t", ("日本語",))
        store.commit()
        store.close()
        store2 = FileStorage(db_path)
        rows = list(store2.scan_rows("t"))
        assert len(rows) == 1
        assert rows[0][1] == ("日本語",)

    def test_long_strings(self, tmp_path: Path) -> None:
        db_path = tmp_path / "test.db"
        store = FileStorage(db_path)
        store.create_table("t", ("val",))
        store.insert_row("t", ("x" * 500,))
        store.commit()
        store.close()
        store2 = FileStorage(db_path)
        rows = list(store2.scan_rows("t"))
        assert len(rows) == 1
        assert rows[0][1] == ("x" * 500,)

    def test_update_and_delete_different_rows(self, tmp_path: Path) -> None:
        db_path = tmp_path / "test.db"
        store = FileStorage(db_path)
        store.create_table("t", ("a",))
        store.insert_row("t", ("keep",))
        store.insert_row("t", ("delete",))
        store.commit()
        rows = list(store.scan_rows("t"))
        store.mark_update("t", rows[0][0], ("updated",))
        store.mark_delete("t", rows[1][0])
        store.commit()
        store.close()
        store2 = FileStorage(db_path)
        rows2 = list(store2.scan_rows("t"))
        assert len(rows2) == 1
        assert rows2[0][1] == ("updated",)

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
        page0.header.next_page = 1
        page1.header.next_page = 2
        page2.header.next_page = 1
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
        max_tables = _tables_per_meta_page("t0000", ("c",))
        total_tables = max_tables + 2
        for i in range(total_tables):
            store.create_table(f"t{i:04d}", ("c",))
        store.insert_row("t0000", ("first",))
        store.insert_row(f"t{total_tables - 1:04d}", ("last",))
        store.commit()
        store.close()
        store2 = FileStorage(db_path)
        for i in range(total_tables):
            assert store2.table_exists(f"t{i:04d}")
        assert list(store2.scan_rows("t0000"))[0][1] == ("first",)
        assert list(store2.scan_rows(f"t{total_tables - 1:04d}"))[0][1] == ("last",)

    def test_metadata_page_growth_after_reload(self, tmp_path: Path) -> None:
        db_path = tmp_path / "test.db"
        store = FileStorage(db_path)
        max_tables = _tables_per_meta_page("t0000", ("c",))
        for i in range(max_tables):
            store.create_table(f"t{i:04d}", ("c",))
        store.commit()
        store.close()

        store2 = FileStorage(db_path)
        store2.create_table(f"t{max_tables:04d}", ("c",))
        store2.insert_row(f"t{max_tables:04d}", ("grown",))
        store2.commit()
        store2.close()

        store3 = FileStorage(db_path)
        assert store3.table_exists(f"t{max_tables:04d}")
        assert list(store3.scan_rows(f"t{max_tables:04d}"))[0][1] == ("grown",)

    def test_non_continuous_page_allocation(self, tmp_path: Path) -> None:
        db_path = tmp_path / "test.db"
        store = FileStorage(db_path)

        payload = "x" * (PAGE_SIZE // 4)
        rows_per_page = _rows_per_page(payload)

        store.create_table("table_a", ("col",))
        for _ in range(rows_per_page):
            store.insert_row("table_a", (payload,))
        store.commit()

        store.create_table("table_b", ("col",))
        store.insert_row("table_b", ("b_row",))
        store.commit()

        store.insert_row("table_a", (payload,))
        store.commit()

        rows_a = list(store.scan_rows("table_a"))
        rows_b = list(store.scan_rows("table_b"))

        assert (
            len(rows_a) == rows_per_page + 1
        ), f"Expected {rows_per_page + 1} rows for table_a, got {len(rows_a)}"
        assert len(rows_b) == 1


class TestFileStorageCompaction:
    def test_compaction_delete_all(self, tmp_path: Path) -> None:
        db_path = tmp_path / "test.db"
        store = FileStorage(db_path)
        store.create_table("t", ("val",))
        payload = "x" * (PAGE_SIZE // 4)
        rows_per_page = _rows_per_page(payload)
        total_rows = rows_per_page * 3 + 1
        for _ in range(total_rows):
            store.insert_row("t", (payload,))
        store.commit()

        rows = list(store.scan_rows("t"))
        for rid, _ in rows:
            store.mark_delete("t", rid)
        store.commit()

        assert list(store.scan_rows("t")) == []
        store.vacuum()
        assert db_path.stat().st_size == PAGE_SIZE * 2

    def test_compaction_complex_deletion_pattern(self, tmp_path: Path) -> None:
        db_path = tmp_path / "test.db"
        store = FileStorage(db_path)
        store.create_table("t", ("val",))
        payload = "x" * (PAGE_SIZE // 5)
        rows_per_page = _rows_per_page(payload)
        total_rows = rows_per_page * 4 + 2
        for _ in range(total_rows):
            store.insert_row("t", (payload,))
        store.commit()

        rows = list(store.scan_rows("t"))
        keep_indices: set[int] = set()
        for i in range(total_rows):
            if i % 2 == 0 and i % 3 == 0:
                keep_indices.add(i)
            if i % 5 == 1:
                keep_indices.add(i)
        for i, (rid, _) in enumerate(rows):
            if i not in keep_indices:
                store.mark_delete("t", rid)
        store.commit()

        assert len(list(store.scan_rows("t"))) == len(keep_indices)
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

        store.create_table("a", ("val",))
        for _ in range(rows_per_page_a * 3 + 1):
            store.insert_row("a", (payload_a,))
        store.create_table("b", ("val",))
        for _ in range(rows_per_page_b * 2 + 2):
            store.insert_row("b", (payload_b,))
        store.create_table("c", ("val",))
        for _ in range(rows_per_page_c * 4 + 3):
            store.insert_row("c", (payload_c,))
        store.commit()

        rows_a = list(store.scan_rows("a"))
        rows_b = list(store.scan_rows("b"))
        rows_c = list(store.scan_rows("c"))

        keep_a = {i for i in range(len(rows_a)) if i % 3 == 0}
        keep_b = {i for i in range(len(rows_b)) if i % 2 == 1 or i % 5 == 0}
        keep_c = {i for i in range(len(rows_c)) if i % 4 == 0 or i % 7 == 3}

        for i, (rid, _) in enumerate(rows_a):
            if i not in keep_a:
                store.mark_delete("a", rid)
        for i, (rid, _) in enumerate(rows_b):
            if i not in keep_b:
                store.mark_delete("b", rid)
        for i, (rid, _) in enumerate(rows_c):
            if i not in keep_c:
                store.mark_delete("c", rid)
        store.commit()
        assert len(list(store.scan_rows("a"))) == len(keep_a)
        assert len(list(store.scan_rows("b"))) == len(keep_b)
        assert len(list(store.scan_rows("c"))) == len(keep_c)
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

        store.create_table("early_data", ("val",))
        for _ in range(rows_per_page * 3):
            store.insert_row("early_data", (data_payload,))

        max_tables = _tables_per_meta_page("t0000", ("c",))
        total_tables = max_tables + 2
        for i in range(total_tables):
            store.create_table(f"t{i:04d}", ("c",))

        store.create_table("late_data", ("val",))
        for _ in range(rows_per_page * 2):
            store.insert_row("late_data", (data_payload,))

        for i in range(total_tables):
            store.insert_row(f"t{i:04d}", (f"val{i}",))
        store.commit()

        for i, (rid, _) in enumerate(store.scan_rows("early_data")):
            if i % 3 != 0:
                store.mark_delete("early_data", rid)
        for i, (rid, _) in enumerate(store.scan_rows("late_data")):
            if i % 4 != 0:
                store.mark_delete("late_data", rid)
        for i in range(total_tables):
            if i % 2 == 0:
                rid, _ = list(store.scan_rows(f"t{i:04d}"))[0]
                store.mark_delete(f"t{i:04d}", rid)
        store.commit()

        early_count = len(list(store.scan_rows("early_data")))
        late_count = len(list(store.scan_rows("late_data")))
        size_before = db_path.stat().st_size
        store.vacuum()
        store.close()

        store2 = FileStorage(db_path)
        assert len(list(store2.scan_rows("early_data"))) == early_count
        assert len(list(store2.scan_rows("late_data"))) == late_count
        for i in range(total_tables):
            name = f"t{i:04d}"
            assert store2.table_exists(name)
            rows = list(store2.scan_rows(name))
            if i % 2 == 0:
                assert rows == []
            else:
                assert rows[0][1] == (f"val{i}",)

        per_data_page = _rows_per_page(data_payload)
        expected_early = (early_count + per_data_page - 1) // per_data_page
        expected_late = (late_count + per_data_page - 1) // per_data_page
        expected_data_pages_for_meta = sum(
            1 for i in range(total_tables) if i % 2 != 0
        )
        per_empty_meta = _tables_per_meta_page("t0000", ("c",))
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
        max_tables = _tables_per_meta_page("t0000", ("c",))
        total_tables = max_tables + 3
        for i in range(total_tables):
            name = f"t{i:04d}"
            store.create_table(name, ("c",))
            store.insert_row(name, (f"v{i}",))
        store.commit()

        for i in range(0, total_tables, 2):
            name = f"t{i:04d}"
            rid, _ = list(store.scan_rows(name))[0]
            store.mark_delete(name, rid)
        store.commit()
        store.vacuum()
        store.close()

        store2 = FileStorage(db_path)
        for i in range(total_tables):
            name = f"t{i:04d}"
            assert store2.table_exists(name)
            rows = list(store2.scan_rows(name))
            if i % 2 == 0:
                assert rows == []
            else:
                assert rows[0][1] == (f"v{i}",)

