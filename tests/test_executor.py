import pytest

from dbms.ast_nodes import (
    Assignment,
    AssignmentColEq,
    CreateTableStmt,
    DeleteStmt,
    InsertStmt,
    SelectStmt,
    UpdateStmt,
    WhereAnd,
    WhereColEq,
    WhereEq,
    WhereOr,
)
from dbms.errors import (
    ColumnMismatchError,
    DuplicateColumnError,
    DuplicateTableError,
    TableNotFoundError,
)
from dbms.executor import Executor, SelectResult
from dbms.in_memory_storage import InMemoryStorage


@pytest.fixture
def store() -> InMemoryStorage:
    return InMemoryStorage()


@pytest.fixture
def executor(store: InMemoryStorage) -> Executor:
    return Executor(store)


class TestCreateTable:
    def test_create_table(self, executor: Executor, store: InMemoryStorage) -> None:
        stmt = CreateTableStmt(name="t", columns=("a", "b"))
        assert executor.execute(stmt) is None
        assert store.table_exists("t")
        assert store.get_columns("t") == ("a", "b")

    def test_duplicate_table(self, executor: Executor) -> None:
        executor.create_table(CreateTableStmt(name="t", columns=("a",)))
        with pytest.raises(DuplicateTableError):
            executor.create_table(CreateTableStmt(name="t", columns=("b",)))

    def test_duplicate_columns(self, executor: Executor) -> None:
        with pytest.raises(DuplicateColumnError):
            executor.create_table(CreateTableStmt(name="t", columns=("a", "a")))

    def test_create_then_select_empty(self, executor: Executor) -> None:
        executor.create_table(CreateTableStmt(name="t", columns=("a", "b")))
        result = executor.select(SelectStmt(table="t", columns="*", where=None))
        assert result.rows == ()
        assert result.columns == ("a", "b")


class TestInsert:
    def test_insert_row(self, executor: Executor, store: InMemoryStorage) -> None:
        executor.create_table(CreateTableStmt(name="t", columns=("a", "b")))
        executor.insert(InsertStmt(table="t", columns=("a", "b"), values=("x", "y")))
        rows = list(store.scan_rows("t"))
        assert len(rows) == 1
        assert rows[0][1] == ("x", "y")

    def test_insert_column_reorder(self, executor: Executor, store: InMemoryStorage) -> None:
        executor.create_table(CreateTableStmt(name="t", columns=("a", "b")))
        executor.insert(InsertStmt(table="t", columns=("b", "a"), values=("y", "x")))
        rows = list(store.scan_rows("t"))
        assert rows[0][1] == ("x", "y")

    def test_table_not_found(self, executor: Executor) -> None:
        with pytest.raises(TableNotFoundError):
            executor.insert(InsertStmt(table="missing", columns=("a",), values=("x",)))

    def test_column_count_mismatch(self, executor: Executor) -> None:
        executor.create_table(CreateTableStmt(name="t", columns=("a", "b")))
        with pytest.raises(ColumnMismatchError):
            executor.insert(InsertStmt(table="t", columns=("a",), values=("x",)))

    def test_insert_column_subset_mismatch(self, executor: Executor) -> None:
        executor.create_table(CreateTableStmt(name="t", columns=("a", "b", "c")))
        with pytest.raises(ColumnMismatchError):
            executor.insert(InsertStmt(table="t", columns=("a", "b"), values=("x", "y")))

    def test_insert_duplicate_rows(self, executor: Executor) -> None:
        executor.create_table(CreateTableStmt(name="t", columns=("a",)))
        executor.insert(InsertStmt(table="t", columns=("a",), values=("x",)))
        executor.insert(InsertStmt(table="t", columns=("a",), values=("x",)))
        result = executor.select(SelectStmt(table="t", columns="*", where=None))
        assert len(result.rows) == 2

    def test_insert_multiple_rows(self, executor: Executor) -> None:
        executor.create_table(CreateTableStmt(name="t", columns=("name", "age")))
        executor.insert(InsertStmt(table="t", columns=("name", "age"), values=("Alice", "30")))
        executor.insert(InsertStmt(table="t", columns=("name", "age"), values=("Bob", "25")))
        executor.insert(InsertStmt(table="t", columns=("name", "age"), values=("Carol", "30")))
        result = executor.select(SelectStmt(table="t", columns="*", where=None))
        assert len(result.rows) == 3

    def test_insert_then_select_roundtrip(self, executor: Executor) -> None:
        executor.create_table(CreateTableStmt(name="t", columns=("a", "b")))
        executor.insert(InsertStmt(table="t", columns=("a", "b"), values=("hello", "world")))
        result = executor.select(SelectStmt(table="t", columns="*", where=None))
        assert result.rows == (("hello", "world"),)

    def test_insert_after_delete(self, executor: Executor) -> None:
        executor.create_table(CreateTableStmt(name="t", columns=("a",)))
        executor.insert(InsertStmt(table="t", columns=("a",), values=("x",)))
        executor.delete(DeleteStmt(table="t", where=None))
        executor.insert(InsertStmt(table="t", columns=("a",), values=("y",)))
        result = executor.select(SelectStmt(table="t", columns="*", where=None))
        assert len(result.rows) == 1
        assert result.rows[0] == ("y",)


class TestSelect:
    def test_select_star(self, executor: Executor) -> None:
        executor.create_table(CreateTableStmt(name="t", columns=("name", "age")))
        executor.insert(InsertStmt(table="t", columns=("name", "age"), values=("Alice", "30")))
        result = executor.select(SelectStmt(table="t", columns="*", where=None))
        assert result.columns == ("name", "age")
        assert result.rows == (("Alice", "30"),)

    def test_select_specific_columns(self, executor: Executor) -> None:
        executor.create_table(CreateTableStmt(name="t", columns=("name", "age")))
        executor.insert(InsertStmt(table="t", columns=("name", "age"), values=("Alice", "30")))
        result = executor.select(SelectStmt(table="t", columns=("name",), where=None))
        assert result.columns == ("name",)
        assert result.rows == (("Alice",),)

    def test_select_column_reorder(self, executor: Executor) -> None:
        executor.create_table(CreateTableStmt(name="t", columns=("name", "age", "city")))
        executor.insert(InsertStmt(table="t", columns=("name", "age", "city"), values=("Alice", "30", "NYC")))
        result = executor.select(SelectStmt(table="t", columns=("city", "name"), where=None))
        assert result.columns == ("city", "name")
        assert result.rows == (("NYC", "Alice"),)

    def test_select_where_eq(self, executor: Executor) -> None:
        executor.create_table(CreateTableStmt(name="t", columns=("name", "age")))
        executor.insert(InsertStmt(table="t", columns=("name", "age"), values=("Alice", "30")))
        executor.insert(InsertStmt(table="t", columns=("name", "age"), values=("Bob", "25")))
        result = executor.select(SelectStmt(table="t", columns="*", where=WhereEq(column="age", value="30")))
        assert len(result.rows) == 1
        assert result.rows[0] == ("Alice", "30")

    def test_select_where_eq_multiple(self, executor: Executor) -> None:
        executor.create_table(CreateTableStmt(name="t", columns=("name", "age")))
        executor.insert(InsertStmt(table="t", columns=("name", "age"), values=("Alice", "30")))
        executor.insert(InsertStmt(table="t", columns=("name", "age"), values=("Bob", "30")))
        executor.insert(InsertStmt(table="t", columns=("name", "age"), values=("Carol", "25")))
        result = executor.select(SelectStmt(table="t", columns="*", where=WhereEq(column="age", value="30")))
        assert len(result.rows) == 2

    def test_select_where_no_match(self, executor: Executor) -> None:
        executor.create_table(CreateTableStmt(name="t", columns=("name",)))
        executor.insert(InsertStmt(table="t", columns=("name",), values=("Alice",)))
        result = executor.select(SelectStmt(table="t", columns="*", where=WhereEq(column="name", value="Nobody")))
        assert result.rows == ()

    def test_select_where_matches_all(self, executor: Executor) -> None:
        executor.create_table(CreateTableStmt(name="t", columns=("city",)))
        executor.insert(InsertStmt(table="t", columns=("city",), values=("NYC",)))
        executor.insert(InsertStmt(table="t", columns=("city",), values=("NYC",)))
        result = executor.select(SelectStmt(table="t", columns="*", where=WhereEq(column="city", value="NYC")))
        assert len(result.rows) == 2

    def test_select_where_and(self, executor: Executor) -> None:
        executor.create_table(CreateTableStmt(name="t", columns=("name", "age", "city")))
        executor.insert(InsertStmt(table="t", columns=("name", "age", "city"), values=("Alice", "30", "NYC")))
        executor.insert(InsertStmt(table="t", columns=("name", "age", "city"), values=("Bob", "30", "LA")))
        result = executor.select(SelectStmt(table="t", columns="*", where=WhereAnd(operands=(WhereEq(column="age", value="30"), WhereEq(column="city", value="NYC")))))
        assert len(result.rows) == 1
        assert result.rows[0] == ("Alice", "30", "NYC")

    def test_select_where_or(self, executor: Executor) -> None:
        executor.create_table(CreateTableStmt(name="t", columns=("name", "age")))
        executor.insert(InsertStmt(table="t", columns=("name", "age"), values=("Alice", "30")))
        executor.insert(InsertStmt(table="t", columns=("name", "age"), values=("Bob", "25")))
        result = executor.select(SelectStmt(table="t", columns="*", where=WhereOr(operands=(WhereEq(column="age", value="30"), WhereEq(column="name", value="Bob")))))
        assert len(result.rows) == 2

    def test_select_where_or_same_row_no_duplicates(self, executor: Executor) -> None:
        executor.create_table(CreateTableStmt(name="t", columns=("name",)))
        executor.insert(InsertStmt(table="t", columns=("name",), values=("Alice",)))
        result = executor.select(SelectStmt(table="t", columns="*", where=WhereOr(operands=(WhereEq(column="name", value="Alice"), WhereEq(column="name", value="Alice")))))
        assert len(result.rows) == 1

    def test_select_where_and_one_side_empty(self, executor: Executor) -> None:
        executor.create_table(CreateTableStmt(name="t", columns=("name",)))
        executor.insert(InsertStmt(table="t", columns=("name",), values=("Alice",)))
        result = executor.select(SelectStmt(table="t", columns="*", where=WhereAnd(operands=(WhereEq(column="name", value="Alice"), WhereEq(column="name", value="Nobody")))))
        assert result.rows == ()

    def test_select_where_col_eq(self, executor: Executor) -> None:
        executor.create_table(CreateTableStmt(name="t", columns=("a", "b")))
        executor.insert(InsertStmt(table="t", columns=("a", "b"), values=("x", "x")))
        executor.insert(InsertStmt(table="t", columns=("a", "b"), values=("x", "y")))
        result = executor.select(SelectStmt(table="t", columns="*", where=WhereColEq(left="a", right="b")))
        assert len(result.rows) == 1
        assert result.rows[0] == ("x", "x")

    def test_select_col_eq_with_eq(self, executor: Executor) -> None:
        executor.create_table(CreateTableStmt(name="t", columns=("a", "b", "c")))
        executor.insert(InsertStmt(table="t", columns=("a", "b", "c"), values=("x", "x", "1")))
        executor.insert(InsertStmt(table="t", columns=("a", "b", "c"), values=("x", "y", "1")))
        result = executor.select(SelectStmt(table="t", columns="*", where=WhereAnd(operands=(WhereColEq(left="a", right="b"), WhereEq(column="c", value="1")))))
        assert len(result.rows) == 1

    def test_select_nested_where(self, executor: Executor) -> None:
        executor.create_table(CreateTableStmt(name="t", columns=("name", "age", "city")))
        executor.insert(InsertStmt(table="t", columns=("name", "age", "city"), values=("Alice", "30", "NYC")))
        executor.insert(InsertStmt(table="t", columns=("name", "age", "city"), values=("Bob", "25", "LA")))
        executor.insert(InsertStmt(table="t", columns=("name", "age", "city"), values=("Carol", "30", "SF")))
        where = WhereAnd(operands=(WhereEq(column="age", value="30"), WhereOr(operands=(WhereEq(column="city", value="NYC"), WhereEq(column="city", value="SF")))))
        result = executor.select(SelectStmt(table="t", columns="*", where=where))
        assert len(result.rows) == 2
        names = {r[0] for r in result.rows}
        assert names == {"Alice", "Carol"}

    def test_empty_table_select(self, executor: Executor) -> None:
        executor.create_table(CreateTableStmt(name="t", columns=("a",)))
        result = executor.select(SelectStmt(table="t", columns="*", where=None))
        assert result.rows == ()

    def test_table_not_found(self, executor: Executor) -> None:
        with pytest.raises(TableNotFoundError):
            executor.select(SelectStmt(table="missing", columns="*", where=None))

    def test_column_not_found(self, executor: Executor) -> None:
        executor.create_table(CreateTableStmt(name="t", columns=("a",)))
        with pytest.raises(ColumnMismatchError):
            executor.select(SelectStmt(table="t", columns=("b",), where=None))

    def test_where_column_not_found(self, executor: Executor) -> None:
        executor.create_table(CreateTableStmt(name="t", columns=("a",)))
        with pytest.raises(ColumnMismatchError):
            executor.select(SelectStmt(table="t", columns="*", where=WhereEq(column="z", value="x")))


class TestUpdate:
    def test_update_with_where(self, store: InMemoryStorage) -> None:
        ex = _make_users_executor(store)
        count = ex.update(UpdateStmt(table="users", assignments=(Assignment(column="city", value="SF"),), where=WhereEq(column="name", value="Alice")))
        assert count == 1
        result = ex.select(SelectStmt(table="users", columns=("city",), where=WhereEq(column="name", value="Alice")))
        assert result.rows == (("SF",),)

    def test_update_col_eq(self, store: InMemoryStorage) -> None:
        ex = _make_users_executor(store)
        count = ex.update(UpdateStmt(table="users", assignments=(AssignmentColEq(left="city", right="name"),), where=WhereEq(column="name", value="Alice")))
        assert count == 1
        result = ex.select(SelectStmt(table="users", columns="*", where=WhereEq(column="name", value="Alice")))
        assert result.rows[0][2] == "Alice"

    def test_update_all_rows(self, store: InMemoryStorage) -> None:
        ex = _make_users_executor(store)
        count = ex.update(UpdateStmt(table="users", assignments=(Assignment(column="city", value="SF"),), where=None))
        assert count == 3
        result = ex.select(SelectStmt(table="users", columns="*", where=None))
        assert all(r[2] == "SF" for r in result.rows)

    def test_update_no_match(self, store: InMemoryStorage) -> None:
        ex = _make_users_executor(store)
        original = ex.select(SelectStmt(table="users", columns="*", where=None))
        count = ex.update(UpdateStmt(table="users", assignments=(Assignment(column="city", value="SF"),), where=WhereEq(column="name", value="Nobody")))
        assert count == 0
        after = ex.select(SelectStmt(table="users", columns="*", where=None))
        assert original.rows == after.rows

    def test_update_multiple_columns(self, store: InMemoryStorage) -> None:
        ex = _make_users_executor(store)
        count = ex.update(UpdateStmt(table="users", assignments=(Assignment(column="age", value="99"), Assignment(column="city", value="SF")), where=WhereEq(column="name", value="Alice")))
        assert count == 1
        result = ex.select(SelectStmt(table="users", columns="*", where=WhereEq(column="name", value="Alice")))
        assert result.rows[0] == ("Alice", "99", "SF")

    def test_update_mixed_assignments(self, store: InMemoryStorage) -> None:
        ex = _make_users_executor(store)
        count = ex.update(UpdateStmt(table="users", assignments=(Assignment(column="city", value="SF"), AssignmentColEq(left="age", right="name")), where=WhereEq(column="name", value="Alice")))
        assert count == 1
        result = ex.select(SelectStmt(table="users", columns="*", where=WhereEq(column="name", value="Alice")))
        assert result.rows[0] == ("Alice", "Alice", "SF")

    def test_update_swap_columns(self, executor: Executor) -> None:
        executor.create_table(CreateTableStmt(name="t", columns=("a", "b")))
        executor.insert(InsertStmt(table="t", columns=("a", "b"), values=("x", "y")))
        executor.update(UpdateStmt(table="t", assignments=(AssignmentColEq(left="a", right="b"), AssignmentColEq(left="b", right="a")), where=None))
        result = executor.select(SelectStmt(table="t", columns="*", where=None))
        assert result.rows == (("y", "x"),)

    def test_update_where_matches_multiple(self, store: InMemoryStorage) -> None:
        ex = _make_users_executor(store)
        count = ex.update(UpdateStmt(table="users", assignments=(Assignment(column="city", value="Boston"),), where=WhereEq(column="city", value="NYC")))
        assert count == 2

    def test_update_nonexistent_column_in_assignments(self, store: InMemoryStorage) -> None:
        ex = _make_users_executor(store)
        with pytest.raises(ColumnMismatchError):
            ex.update(UpdateStmt(table="users", assignments=(Assignment(column="zzz", value="x"),), where=None))

    def test_update_col_eq_nonexistent_column(self, store: InMemoryStorage) -> None:
        ex = _make_users_executor(store)
        with pytest.raises(ColumnMismatchError):
            ex.update(UpdateStmt(table="users", assignments=(AssignmentColEq(left="city", right="zzz"),), where=None))

    def test_table_not_found(self, executor: Executor) -> None:
        with pytest.raises(TableNotFoundError):
            executor.update(UpdateStmt(table="missing", assignments=(Assignment(column="a", value="x"),), where=None))

    def test_update_same_value_noop(self, store: InMemoryStorage) -> None:
        ex = _make_users_executor(store)
        original = ex.select(SelectStmt(table="users", columns="*", where=None))
        count = ex.update(UpdateStmt(table="users", assignments=(Assignment(column="city", value="NYC"),), where=WhereEq(column="name", value="Alice")))
        assert count == 1
        after = ex.select(SelectStmt(table="users", columns="*", where=None))
        assert original.rows == after.rows


class TestDelete:
    def test_delete_with_where(self, store: InMemoryStorage) -> None:
        ex = _make_users_executor(store)
        count = ex.delete(DeleteStmt(table="users", where=WhereEq(column="name", value="Alice")))
        assert count == 1
        result = ex.select(SelectStmt(table="users", columns="*", where=None))
        assert len(result.rows) == 2

    def test_delete_all(self, store: InMemoryStorage) -> None:
        ex = _make_users_executor(store)
        count = ex.delete(DeleteStmt(table="users", where=None))
        assert count == 3
        result = ex.select(SelectStmt(table="users", columns="*", where=None))
        assert result.rows == ()

    def test_delete_no_match(self, store: InMemoryStorage) -> None:
        ex = _make_users_executor(store)
        original = ex.select(SelectStmt(table="users", columns="*", where=None))
        count = ex.delete(DeleteStmt(table="users", where=WhereEq(column="name", value="Nobody")))
        assert count == 0
        after = ex.select(SelectStmt(table="users", columns="*", where=None))
        assert original.rows == after.rows

    def test_delete_then_select_deleted_value(self, store: InMemoryStorage) -> None:
        ex = _make_users_executor(store)
        ex.delete(DeleteStmt(table="users", where=WhereEq(column="name", value="Alice")))
        result = ex.select(SelectStmt(table="users", columns="*", where=WhereEq(column="name", value="Alice")))
        assert result.rows == ()

    def test_table_not_found(self, executor: Executor) -> None:
        with pytest.raises(TableNotFoundError):
            executor.delete(DeleteStmt(table="missing", where=None))


class TestLifecycleSequences:
    def test_crud_cycle(self, executor: Executor) -> None:
        executor.create_table(CreateTableStmt(name="t", columns=("a", "b")))
        executor.insert(InsertStmt(table="t", columns=("a", "b"), values=("x", "y")))
        result = executor.select(SelectStmt(table="t", columns="*", where=None))
        assert result.rows == (("x", "y"),)

        executor.update(UpdateStmt(table="t", assignments=(Assignment(column="b", value="z"),), where=WhereEq(column="a", value="x")))
        result = executor.select(SelectStmt(table="t", columns="*", where=None))
        assert result.rows == (("x", "z"),)

        executor.delete(DeleteStmt(table="t", where=WhereEq(column="a", value="x")))
        result = executor.select(SelectStmt(table="t", columns="*", where=None))
        assert result.rows == ()

    def test_multi_row_mixed_operations(self, executor: Executor) -> None:
        executor.create_table(CreateTableStmt(name="t", columns=("name", "age", "city")))
        executor.insert(InsertStmt(table="t", columns=("name", "age", "city"), values=("Alice", "30", "NYC")))
        executor.insert(InsertStmt(table="t", columns=("name", "age", "city"), values=("Bob", "25", "LA")))
        executor.insert(InsertStmt(table="t", columns=("name", "age", "city"), values=("Carol", "30", "NYC")))

        executor.update(UpdateStmt(table="t", assignments=(Assignment(column="city", value="SF"),), where=WhereEq(column="age", value="30")))
        result = executor.select(SelectStmt(table="t", columns="*", where=WhereEq(column="age", value="30")))
        assert all(r[2] == "SF" for r in result.rows)

        bob_result = executor.select(SelectStmt(table="t", columns="*", where=WhereEq(column="name", value="Bob")))
        assert bob_result.rows[0][2] == "LA"

        executor.delete(DeleteStmt(table="t", where=WhereEq(column="city", value="LA")))
        result = executor.select(SelectStmt(table="t", columns="*", where=None))
        assert len(result.rows) == 2

    def test_delete_then_reinsert(self, executor: Executor) -> None:
        executor.create_table(CreateTableStmt(name="t", columns=("a", "b")))
        executor.insert(InsertStmt(table="t", columns=("a", "b"), values=("x", "y")))
        executor.delete(DeleteStmt(table="t", where=None))
        executor.insert(InsertStmt(table="t", columns=("a", "b"), values=("x", "y")))
        result = executor.select(SelectStmt(table="t", columns="*", where=WhereEq(column="a", value="x")))
        assert len(result.rows) == 1

    def test_update_changing_where_column(self, store: InMemoryStorage) -> None:
        ex = _make_users_executor(store)
        ex.update(UpdateStmt(table="users", assignments=(Assignment(column="name", value="Zack"),), where=WhereEq(column="name", value="Alice")))
        result = ex.select(SelectStmt(table="users", columns="*", where=WhereEq(column="name", value="Alice")))
        assert len(result.rows) == 0
        result = ex.select(SelectStmt(table="users", columns="*", where=WhereEq(column="name", value="Zack")))
        assert len(result.rows) == 1

    def test_sequential_updates_accumulate(self, store: InMemoryStorage) -> None:
        ex = _make_users_executor(store)
        ex.update(UpdateStmt(table="users", assignments=(Assignment(column="city", value="SF"),), where=WhereEq(column="name", value="Alice")))
        ex.update(UpdateStmt(table="users", assignments=(Assignment(column="age", value="99"),), where=WhereEq(column="name", value="Alice")))
        result = ex.select(SelectStmt(table="users", columns="*", where=WhereEq(column="name", value="Alice")))
        assert result.rows[0] == ("Alice", "99", "SF")

    def test_complex_nested_where_across_operations(self, executor: Executor) -> None:
        executor.create_table(CreateTableStmt(name="t", columns=("name", "age", "city")))
        executor.insert(InsertStmt(table="t", columns=("name", "age", "city"), values=("Alice", "30", "NYC")))
        executor.insert(InsertStmt(table="t", columns=("name", "age", "city"), values=("Bob", "25", "LA")))
        executor.insert(InsertStmt(table="t", columns=("name", "age", "city"), values=("Carol", "30", "SF")))

        where_or = WhereOr(operands=(WhereEq(column="name", value="Alice"), WhereAnd(operands=(WhereEq(column="age", value="30"), WhereEq(column="city", value="SF")))))
        result = executor.select(SelectStmt(table="t", columns="*", where=where_or))
        assert len(result.rows) == 2
        names = {r[0] for r in result.rows}
        assert names == {"Alice", "Carol"}

        executor.update(UpdateStmt(table="t", assignments=(Assignment(column="age", value="99"),), where=where_or))
        result = executor.select(SelectStmt(table="t", columns="*", where=WhereEq(column="age", value="99")))
        assert len(result.rows) == 2

        executor.delete(DeleteStmt(table="t", where=WhereAnd(operands=(WhereEq(column="city", value="NYC"), WhereEq(column="age", value="99")))))
        result = executor.select(SelectStmt(table="t", columns="*", where=None))
        assert len(result.rows) == 2

    def test_failed_operation_leaves_state_unchanged(self, executor: Executor) -> None:
        executor.create_table(CreateTableStmt(name="t", columns=("a", "b")))
        executor.insert(InsertStmt(table="t", columns=("a", "b"), values=("x", "y")))
        original = executor.select(SelectStmt(table="t", columns="*", where=None))
        with pytest.raises(ColumnMismatchError):
            executor.select(SelectStmt(table="t", columns=("zzz",), where=None))
        after = executor.select(SelectStmt(table="t", columns="*", where=None))
        assert original.rows == after.rows

    def test_delete_no_match_preserves_data(self, executor: Executor) -> None:
        executor.create_table(CreateTableStmt(name="t", columns=("name",)))
        for n in ("Alice", "Bob", "Carol"):
            executor.insert(InsertStmt(table="t", columns=("name",), values=(n,)))
        original = executor.select(SelectStmt(table="t", columns="*", where=None))
        count = executor.delete(DeleteStmt(table="t", where=WhereEq(column="name", value="Nobody")))
        assert count == 0
        after = executor.select(SelectStmt(table="t", columns="*", where=None))
        assert original.rows == after.rows


def _make_users_executor(store: InMemoryStorage) -> Executor:
    store.create_table("users", ("name", "age", "city"))
    store.insert_row("users", ("Alice", "30", "NYC"))
    store.insert_row("users", ("Bob", "25", "LA"))
    store.insert_row("users", ("Carol", "30", "NYC"))
    return Executor(store)