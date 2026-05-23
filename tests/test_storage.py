import pytest

from dbms.errors import ColumnMismatchError, DuplicateTableError, TableNotFoundError
from dbms.storage import InMemoryStorage, RowId


@pytest.fixture
def store() -> InMemoryStorage:
    return InMemoryStorage()


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
            store.mark_update("missing", RowId(0), ("z",))


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
            store.mark_delete("missing", RowId(0))


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