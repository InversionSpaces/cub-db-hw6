import pytest
from pathlib import Path

from dbms.ast_nodes import (
    Assignment,
    AssignmentColEq,
    BoolValue,
    ColumnDef,
    ColumnType,
    CreateTableStmt,
    DeleteStmt,
    InsertStmt,
    IntValue,
    Row,
    SelectStmt,
    Statement,
    TextValue,
    UpdateStmt,
    Value,
    WhereAnd,
    WhereColEq,
    WhereEq,
    WhereOr,
)
from dbms.storage_protocol import SBoolValue, SIntValue, StorageColumnDef, StorageColumnType, StorageRow, STextValue


def _scd(name: str, stype: StorageColumnType = StorageColumnType.TEXT) -> StorageColumnDef:
    return StorageColumnDef(name=name, type=stype)


def _st(v: str) -> STextValue:
    return STextValue(value=v)


def _si(v: int) -> SIntValue:
    return SIntValue(value=v)


def _sb(v: bool) -> SBoolValue:
    return SBoolValue(value=v)


from dbms.errors import (
    ColumnMismatchError,
    DuplicateColumnError,
    DuplicateTableError,
    TableNotFoundError,
    TypeMismatchError,
)
from dbms.executor import Executor, SelectResult
from dbms.storage import FileStorage
from dbms.storage_protocol import TableName


@pytest.fixture
def store(tmp_path: Path) -> FileStorage:
    return FileStorage(tmp_path / "test.db")


@pytest.fixture
def executor(store: FileStorage) -> Executor:
    return Executor(store)


class TestCreateTable:
    def test_create_table(self, executor: Executor, store: FileStorage) -> None:
        cols = (
            ColumnDef(name="a", type=ColumnType.TEXT),
            ColumnDef(name="b", type=ColumnType.INT),
        )
        stmt = CreateTableStmt(name="t", columns=cols)
        assert executor.execute(stmt) is None
        result = executor.select(SelectStmt(table="t", columns="*", where=None))
        assert result.columns == ("a", "b")
        assert len(result.rows) == 0

    def test_duplicate_table(self, executor: Executor) -> None:
        cols = (ColumnDef(name="a", type=ColumnType.TEXT),)
        executor.create_table(CreateTableStmt(name="t", columns=cols))
        with pytest.raises(DuplicateTableError):
            executor.create_table(CreateTableStmt(name="t", columns=cols))

    def test_duplicate_columns(self, executor: Executor) -> None:
        cols = (
            ColumnDef(name="a", type=ColumnType.INT),
            ColumnDef(name="a", type=ColumnType.INT),
        )
        with pytest.raises(DuplicateColumnError):
            executor.create_table(CreateTableStmt(name="t", columns=cols))

    def test_create_then_select_empty(self, executor: Executor) -> None:
        cols = (
            ColumnDef(name="a", type=ColumnType.TEXT),
            ColumnDef(name="b", type=ColumnType.INT),
        )
        executor.create_table(CreateTableStmt(name="t", columns=cols))
        result = executor.select(SelectStmt(table="t", columns="*", where=None))
        assert result.rows == ()
        assert result.columns == ("a", "b")


class TestInsert:
    def test_insert_row(self, executor: Executor, store: FileStorage) -> None:
        cols = (
            ColumnDef(name="a", type=ColumnType.TEXT),
            ColumnDef(name="b", type=ColumnType.INT),
        )
        executor.create_table(CreateTableStmt(name="t", columns=cols))
        executor.insert(InsertStmt(
            table="t",
            columns=("a", "b"),
            values=(TextValue(value="x"), IntValue(value=42))
        ))
        result = executor.select(SelectStmt(table="t", columns="*", where=None))
        assert len(result.rows) == 1
        assert result.rows[0][0] == TextValue(value="x")
        assert result.rows[0][1] == IntValue(value=42)

    def test_insert_column_reorder(self, executor: Executor, store: FileStorage) -> None:
        cols = (
            ColumnDef(name="a", type=ColumnType.TEXT),
            ColumnDef(name="b", type=ColumnType.INT),
        )
        executor.create_table(CreateTableStmt(name="t", columns=cols))
        executor.insert(InsertStmt(
            table="t",
            columns=("b", "a"),
            values=(IntValue(value=42), TextValue(value="x"))
        ))
        result = executor.select(SelectStmt(table="t", columns="*", where=None))
        assert len(result.rows) == 1
        assert result.rows[0][0] == TextValue(value="x")
        assert result.rows[0][1] == IntValue(value=42)

    def test_table_not_found(self, executor: Executor) -> None:
        with pytest.raises(TableNotFoundError):
            executor.insert(InsertStmt(
                table="missing",
                columns=("a",),
                values=(TextValue(value="x"),)
            ))

    def test_column_count_mismatch(self, executor: Executor) -> None:
        cols = (
            ColumnDef(name="a", type=ColumnType.TEXT),
            ColumnDef(name="b", type=ColumnType.INT),
        )
        executor.create_table(CreateTableStmt(name="t", columns=cols))
        with pytest.raises(ColumnMismatchError):
            executor.insert(InsertStmt(
                table="t",
                columns=("a",),
                values=(TextValue(value="x"),)
            ))

    def test_insert_column_subset_mismatch(self, executor: Executor) -> None:
        cols = (
            ColumnDef(name="a", type=ColumnType.TEXT),
            ColumnDef(name="b", type=ColumnType.INT),
            ColumnDef(name="c", type=ColumnType.BOOL),
        )
        executor.create_table(CreateTableStmt(name="t", columns=cols))
        with pytest.raises(ColumnMismatchError):
            executor.insert(InsertStmt(
                table="t",
                columns=("a", "b"),
                values=(TextValue(value="x"), IntValue(value=1))
            ))

    def test_type_mismatch_on_insert(self, executor: Executor) -> None:
        cols = (ColumnDef(name="a", type=ColumnType.INT),)
        executor.create_table(CreateTableStmt(name="t", columns=cols))
        with pytest.raises(TypeMismatchError) as exc_info:
            executor.insert(InsertStmt(
                table="t",
                columns=("a",),
                values=(TextValue(value="not_an_int"),)
            ))
        assert exc_info.value.column == "a"
        assert exc_info.value.expected == "INT"

    def test_insert_bool_value(self, executor: Executor, store: FileStorage) -> None:
        cols = (ColumnDef(name="active", type=ColumnType.BOOL),)
        executor.create_table(CreateTableStmt(name="t", columns=cols))
        executor.insert(InsertStmt(
            table="t",
            columns=("active",),
            values=(BoolValue(value=True),)
        ))
        executor.insert(InsertStmt(
            table="t",
            columns=("active",),
            values=(BoolValue(value=False),)
        ))
        result = executor.select(SelectStmt(table="t", columns="*", where=None))
        assert len(result.rows) == 2
        assert result.rows[0][0] == BoolValue(value=True)
        assert result.rows[1][0] == BoolValue(value=False)

    def test_insert_bool_type_mismatch(self, executor: Executor) -> None:
        cols = (ColumnDef(name="active", type=ColumnType.BOOL),)
        executor.create_table(CreateTableStmt(name="t", columns=cols))
        with pytest.raises(TypeMismatchError):
            executor.insert(InsertStmt(
                table="t",
                columns=("active",),
                values=(IntValue(value=1),)
            ))
        with pytest.raises(TypeMismatchError):
            executor.insert(InsertStmt(
                table="t",
                columns=("active",),
                values=(TextValue(value="true"),)
            ))

    def test_insert_int_into_text_column(self, executor: Executor) -> None:
        cols = (ColumnDef(name="a", type=ColumnType.TEXT),)
        executor.create_table(CreateTableStmt(name="t", columns=cols))
        with pytest.raises(TypeMismatchError) as exc_info:
            executor.insert(InsertStmt(
                table="t", columns=("a",),
                values=(IntValue(value=1),)
            ))
        assert exc_info.value.column == "a"
        assert exc_info.value.expected == "TEXT"

    def test_insert_bool_into_text_column(self, executor: Executor) -> None:
        cols = (ColumnDef(name="a", type=ColumnType.TEXT),)
        executor.create_table(CreateTableStmt(name="t", columns=cols))
        with pytest.raises(TypeMismatchError):
            executor.insert(InsertStmt(
                table="t", columns=("a",),
                values=(BoolValue(value=True),)
            ))

    def test_insert_int_zero(self, executor: Executor) -> None:
        cols = (ColumnDef(name="a", type=ColumnType.INT),)
        executor.create_table(CreateTableStmt(name="t", columns=cols))
        executor.insert(InsertStmt(table="t", columns=("a",), values=(IntValue(value=0),)))
        result = executor.select(SelectStmt(
            table="t", columns="*",
            where=WhereEq(column="a", value=IntValue(value=0)),
        ))
        assert len(result.rows) == 1
        assert result.rows[0][0] == IntValue(value=0)

    def test_insert_int_negative(self, executor: Executor) -> None:
        cols = (ColumnDef(name="a", type=ColumnType.INT),)
        executor.create_table(CreateTableStmt(name="t", columns=cols))
        executor.insert(InsertStmt(table="t", columns=("a",), values=(IntValue(value=-5),)))
        result = executor.select(SelectStmt(
            table="t", columns="*",
            where=WhereEq(column="a", value=IntValue(value=-5)),
        ))
        assert len(result.rows) == 1
        assert result.rows[0][0] == IntValue(value=-5)

    def test_insert_empty_text(self, executor: Executor) -> None:
        cols = (ColumnDef(name="a", type=ColumnType.TEXT),)
        executor.create_table(CreateTableStmt(name="t", columns=cols))
        executor.insert(InsertStmt(table="t", columns=("a",), values=(TextValue(value=""),)))
        executor.insert(InsertStmt(table="t", columns=("a",), values=(TextValue(value="hello"),)))
        result = executor.select(SelectStmt(
            table="t", columns="*",
            where=WhereEq(column="a", value=TextValue(value="")),
        ))
        assert len(result.rows) == 1
        assert result.rows[0][0] == TextValue(value="")

    def test_insert_duplicate_rows(self, executor: Executor) -> None:
        cols = (ColumnDef(name="a", type=ColumnType.TEXT),)
        executor.create_table(CreateTableStmt(name="t", columns=cols))
        executor.insert(InsertStmt(
            table="t",
            columns=("a",),
            values=(TextValue(value="x"),)
        ))
        executor.insert(InsertStmt(
            table="t",
            columns=("a",),
            values=(TextValue(value="x"),)
        ))
        result = executor.select(SelectStmt(table="t", columns="*", where=None))
        assert len(result.rows) == 2
        assert all(r[0] == TextValue(value="x") for r in result.rows)

    def test_insert_multiple_rows(self, executor: Executor) -> None:
        cols = (
            ColumnDef(name="name", type=ColumnType.TEXT),
            ColumnDef(name="age", type=ColumnType.INT),
        )
        executor.create_table(CreateTableStmt(name="t", columns=cols))
        executor.insert(InsertStmt(
            table="t",
            columns=("name", "age"),
            values=(TextValue(value="Alice"), IntValue(value=30))
        ))
        executor.insert(InsertStmt(
            table="t",
            columns=("name", "age"),
            values=(TextValue(value="Bob"), IntValue(value=25))
        ))
        executor.insert(InsertStmt(
            table="t",
            columns=("name", "age"),
            values=(TextValue(value="Carol"), IntValue(value=30))
        ))
        result = executor.select(SelectStmt(table="t", columns="*", where=None))
        assert len(result.rows) == 3
        names = {r[0] for r in result.rows}
        assert names == {TextValue(value="Alice"), TextValue(value="Bob"), TextValue(value="Carol")}


class TestSelect:
    def test_select_star(self, executor: Executor) -> None:
        cols = (
            ColumnDef(name="name", type=ColumnType.TEXT),
            ColumnDef(name="age", type=ColumnType.INT),
        )
        executor.create_table(CreateTableStmt(name="t", columns=cols))
        executor.insert(InsertStmt(
            table="t",
            columns=("name", "age"),
            values=(TextValue(value="Alice"), IntValue(value=30))
        ))
        result = executor.select(SelectStmt(table="t", columns="*", where=None))
        assert result.columns == ("name", "age")
        assert result.rows == ((TextValue(value="Alice"), IntValue(value=30)),)

    def test_select_specific_columns(self, executor: Executor) -> None:
        cols = (
            ColumnDef(name="name", type=ColumnType.TEXT),
            ColumnDef(name="age", type=ColumnType.INT),
        )
        executor.create_table(CreateTableStmt(name="t", columns=cols))
        executor.insert(InsertStmt(
            table="t",
            columns=("name", "age"),
            values=(TextValue(value="Alice"), IntValue(value=30))
        ))
        result = executor.select(SelectStmt(
            table="t",
            columns=("name",),
            where=None
        ))
        assert result.columns == ("name",)
        assert result.rows == ((TextValue(value="Alice"),),)

    def test_select_column_reorder(self, executor: Executor) -> None:
        cols = (
            ColumnDef(name="name", type=ColumnType.TEXT),
            ColumnDef(name="age", type=ColumnType.INT),
            ColumnDef(name="city", type=ColumnType.TEXT),
        )
        executor.create_table(CreateTableStmt(name="t", columns=cols))
        executor.insert(InsertStmt(
            table="t",
            columns=("name", "age", "city"),
            values=(TextValue(value="Alice"), IntValue(value=30), TextValue(value="NYC"))
        ))
        result = executor.select(SelectStmt(
            table="t",
            columns=("city", "name"),
            where=None
        ))
        assert result.columns == ("city", "name")
        assert result.rows == ((TextValue(value="NYC"), TextValue(value="Alice")),)

    def test_select_where_eq(self, executor: Executor) -> None:
        cols = (
            ColumnDef(name="name", type=ColumnType.TEXT),
            ColumnDef(name="age", type=ColumnType.INT),
        )
        executor.create_table(CreateTableStmt(name="t", columns=cols))
        executor.insert(InsertStmt(
            table="t",
            columns=("name", "age"),
            values=(TextValue(value="Alice"), IntValue(value=30))
        ))
        executor.insert(InsertStmt(
            table="t",
            columns=("name", "age"),
            values=(TextValue(value="Bob"), IntValue(value=25))
        ))
        result = executor.select(SelectStmt(
            table="t",
            columns="*",
            where=WhereEq(column="age", value=IntValue(value=30))
        ))
        assert len(result.rows) == 1
        assert result.rows[0] == (TextValue(value="Alice"), IntValue(value=30))

    def test_select_where_eq_multiple(self, executor: Executor) -> None:
        cols = (
            ColumnDef(name="name", type=ColumnType.TEXT),
            ColumnDef(name="age", type=ColumnType.INT),
        )
        executor.create_table(CreateTableStmt(name="t", columns=cols))
        executor.insert(InsertStmt(
            table="t",
            columns=("name", "age"),
            values=(TextValue(value="Alice"), IntValue(value=30))
        ))
        executor.insert(InsertStmt(
            table="t",
            columns=("name", "age"),
            values=(TextValue(value="Bob"), IntValue(value=30))
        ))
        executor.insert(InsertStmt(
            table="t",
            columns=("name", "age"),
            values=(TextValue(value="Carol"), IntValue(value=25))
        ))
        result = executor.select(SelectStmt(
            table="t",
            columns="*",
            where=WhereEq(column="age", value=IntValue(value=30))
        ))
        assert len(result.rows) == 2
        names = {r[0] for r in result.rows}
        assert names == {TextValue(value="Alice"), TextValue(value="Bob")}

    def test_select_where_no_match(self, executor: Executor) -> None:
        cols = (ColumnDef(name="name", type=ColumnType.TEXT),)
        executor.create_table(CreateTableStmt(name="t", columns=cols))
        executor.insert(InsertStmt(
            table="t",
            columns=("name",),
            values=(TextValue(value="Alice"),)
        ))
        result = executor.select(SelectStmt(
            table="t",
            columns="*",
            where=WhereEq(column="name", value=TextValue(value="Nobody"))
        ))
        assert result.rows == ()

    def test_select_where_matches_all(self, executor: Executor) -> None:
        cols = (ColumnDef(name="city", type=ColumnType.TEXT),)
        executor.create_table(CreateTableStmt(name="t", columns=cols))
        executor.insert(InsertStmt(
            table="t",
            columns=("city",),
            values=(TextValue(value="NYC"),)
        ))
        executor.insert(InsertStmt(
            table="t",
            columns=("city",),
            values=(TextValue(value="NYC"),)
        ))
        result = executor.select(SelectStmt(
            table="t",
            columns="*",
            where=WhereEq(column="city", value=TextValue(value="NYC"))
        ))
        assert all(r[0] == TextValue(value="NYC") for r in result.rows)

    def test_select_where_and(self, executor: Executor) -> None:
        cols = (
            ColumnDef(name="name", type=ColumnType.TEXT),
            ColumnDef(name="age", type=ColumnType.INT),
            ColumnDef(name="city", type=ColumnType.TEXT),
        )
        executor.create_table(CreateTableStmt(name="t", columns=cols))
        executor.insert(InsertStmt(
            table="t",
            columns=("name", "age", "city"),
            values=(TextValue(value="Alice"), IntValue(value=30), TextValue(value="NYC"))
        ))
        executor.insert(InsertStmt(
            table="t",
            columns=("name", "age", "city"),
            values=(TextValue(value="Bob"), IntValue(value=30), TextValue(value="LA"))
        ))
        result = executor.select(SelectStmt(
            table="t",
            columns="*",
            where=WhereAnd(operands=(
                WhereEq(column="age", value=IntValue(value=30)),
                WhereEq(column="city", value=TextValue(value="NYC"))
            ))
        ))
        assert len(result.rows) == 1
        assert result.rows[0] == (
            TextValue(value="Alice"),
            IntValue(value=30),
            TextValue(value="NYC")
        )

    def test_select_where_or(self, executor: Executor) -> None:
        cols = (
            ColumnDef(name="name", type=ColumnType.TEXT),
            ColumnDef(name="age", type=ColumnType.INT),
        )
        executor.create_table(CreateTableStmt(name="t", columns=cols))
        executor.insert(InsertStmt(
            table="t",
            columns=("name", "age"),
            values=(TextValue(value="Alice"), IntValue(value=30))
        ))
        executor.insert(InsertStmt(
            table="t",
            columns=("name", "age"),
            values=(TextValue(value="Bob"), IntValue(value=25))
        ))
        result = executor.select(SelectStmt(
            table="t",
            columns="*",
            where=WhereOr(operands=(
                WhereEq(column="age", value=IntValue(value=30)),
                WhereEq(column="name", value=TextValue(value="Bob"))
            ))
        ))
        assert len(result.rows) == 2
        names = {r[0] for r in result.rows}
        assert names == {TextValue(value="Alice"), TextValue(value="Bob")}

    def test_select_where_or_same_row_no_duplicates(self, executor: Executor) -> None:
        cols = (ColumnDef(name="name", type=ColumnType.TEXT),)
        executor.create_table(CreateTableStmt(name="t", columns=cols))
        executor.insert(InsertStmt(
            table="t",
            columns=("name",),
            values=(TextValue(value="Alice"),)
        ))
        result = executor.select(SelectStmt(
            table="t",
            columns="*",
            where=WhereOr(operands=(
                WhereEq(column="name", value=TextValue(value="Alice")),
                WhereEq(column="name", value=TextValue(value="Alice"))
            ))
        ))
        assert len(result.rows) == 1

    def test_select_where_and_one_side_empty(self, executor: Executor) -> None:
        cols = (ColumnDef(name="name", type=ColumnType.TEXT),)
        executor.create_table(CreateTableStmt(name="t", columns=cols))
        executor.insert(InsertStmt(
            table="t",
            columns=("name",),
            values=(TextValue(value="Alice"),)
        ))
        result = executor.select(SelectStmt(
            table="t",
            columns="*",
            where=WhereAnd(operands=(
                WhereEq(column="name", value=TextValue(value="Alice")),
                WhereEq(column="name", value=TextValue(value="Nobody"))
            ))
        ))
        assert result.rows == ()

    def test_select_where_col_eq(self, executor: Executor) -> None:
        cols = (
            ColumnDef(name="a", type=ColumnType.TEXT),
            ColumnDef(name="b", type=ColumnType.TEXT),
        )
        executor.create_table(CreateTableStmt(name="t", columns=cols))
        executor.insert(InsertStmt(
            table="t",
            columns=("a", "b"),
            values=(TextValue(value="x"), TextValue(value="x"))
        ))
        executor.insert(InsertStmt(
            table="t",
            columns=("a", "b"),
            values=(TextValue(value="x"), TextValue(value="y"))
        ))
        result = executor.select(SelectStmt(
            table="t",
            columns="*",
            where=WhereColEq(left="a", right="b")
        ))
        assert len(result.rows) == 1
        assert result.rows[0] == (TextValue(value="x"), TextValue(value="x"))

    def test_select_col_eq_with_eq(self, executor: Executor) -> None:
        cols = (
            ColumnDef(name="a", type=ColumnType.TEXT),
            ColumnDef(name="b", type=ColumnType.TEXT),
            ColumnDef(name="c", type=ColumnType.TEXT),
        )
        executor.create_table(CreateTableStmt(name="t", columns=cols))
        executor.insert(InsertStmt(
            table="t",
            columns=("a", "b", "c"),
            values=(TextValue(value="x"), TextValue(value="x"), TextValue(value="1"))
        ))
        executor.insert(InsertStmt(
            table="t",
            columns=("a", "b", "c"),
            values=(TextValue(value="x"), TextValue(value="y"), TextValue(value="1"))
        ))
        result = executor.select(SelectStmt(
            table="t",
            columns="*",
            where=WhereAnd(operands=(
                WhereColEq(left="a", right="b"),
                WhereEq(column="c", value=TextValue(value="1"))
            ))
        ))
        assert len(result.rows) == 1

    def test_select_nested_where(self, executor: Executor) -> None:
        cols = (
            ColumnDef(name="name", type=ColumnType.TEXT),
            ColumnDef(name="age", type=ColumnType.INT),
            ColumnDef(name="city", type=ColumnType.TEXT),
        )
        executor.create_table(CreateTableStmt(name="t", columns=cols))
        executor.insert(InsertStmt(
            table="t",
            columns=("name", "age", "city"),
            values=(TextValue(value="Alice"), IntValue(value=30), TextValue(value="NYC"))
        ))
        executor.insert(InsertStmt(
            table="t",
            columns=("name", "age", "city"),
            values=(TextValue(value="Bob"), IntValue(value=25), TextValue(value="LA"))
        ))
        executor.insert(InsertStmt(
            table="t",
            columns=("name", "age", "city"),
            values=(TextValue(value="Carol"), IntValue(value=30), TextValue(value="SF"))
        ))
        where = WhereAnd(operands=(
            WhereEq(column="age", value=IntValue(value=30)),
            WhereOr(operands=(
                WhereEq(column="city", value=TextValue(value="NYC")),
                WhereEq(column="city", value=TextValue(value="SF"))
            ))
        ))
        result = executor.select(SelectStmt(table="t", columns="*", where=where))
        assert len(result.rows) == 2
        names = {r[0].value for r in result.rows}
        assert names == {"Alice", "Carol"}

    def test_table_not_found(self, executor: Executor) -> None:
        with pytest.raises(TableNotFoundError):
            executor.select(SelectStmt(table="missing", columns="*", where=None))

    def test_column_not_found(self, executor: Executor) -> None:
        cols = (ColumnDef(name="a", type=ColumnType.TEXT),)
        executor.create_table(CreateTableStmt(name="t", columns=cols))
        with pytest.raises(ColumnMismatchError):
            executor.select(SelectStmt(
                table="t",
                columns=("b",),
                where=None
            ))

    def test_where_column_not_found(self, executor: Executor) -> None:
        cols = (ColumnDef(name="a", type=ColumnType.TEXT),)
        executor.create_table(CreateTableStmt(name="t", columns=cols))
        with pytest.raises(ColumnMismatchError):
            executor.select(SelectStmt(
                table="t",
                columns="*",
                where=WhereEq(column="z", value=TextValue(value="x"))
            ))

    def test_where_type_mismatch(self, executor: Executor) -> None:
        cols = (ColumnDef(name="a", type=ColumnType.INT),)
        executor.create_table(CreateTableStmt(name="t", columns=cols))
        executor.insert(InsertStmt(
            table="t",
            columns=("a",),
            values=(IntValue(value=1),)
        ))
        with pytest.raises(TypeMismatchError) as exc_info:
            executor.select(SelectStmt(
                table="t",
                columns="*",
                where=WhereEq(column="a", value=TextValue(value="x"))
            ))
        assert exc_info.value.column == "a"
        assert exc_info.value.expected == "INT"


def _make_users_executor(store: FileStorage) -> Executor:
    cols = (
        _scd("name", StorageColumnType.TEXT),
        _scd("age", StorageColumnType.INT),
        _scd("city", StorageColumnType.TEXT),
    )
    store.create_table(TableName("users"), cols)
    store.insert_row(TableName("users"), (
        _st("Alice"),
        _si(30),
        _st("NYC")
    ))
    store.insert_row(TableName("users"), (
        _st("Bob"),
        _si(25),
        _st("LA")
    ))
    store.insert_row(TableName("users"), (
        _st("Carol"),
        _si(30),
        _st("NYC")
    ))
    store.commit()
    return Executor(store)


class TestUpdate:
    def test_update_with_where(self, store: FileStorage) -> None:
        ex = _make_users_executor(store)
        count = ex.update(UpdateStmt(
            table="users",
            assignments=(Assignment(column="city", value=TextValue(value="SF")),),
            where=WhereEq(column="name", value=TextValue(value="Alice"))
        ))
        assert count == 1
        result = ex.select(SelectStmt(
            table="users",
            columns=("city",),
            where=WhereEq(column="name", value=TextValue(value="Alice"))
        ))
        assert result.rows == ((TextValue(value="SF"),),)

    def test_update_col_eq(self, store: FileStorage) -> None:
        ex = _make_users_executor(store)
        count = ex.update(UpdateStmt(
            table="users",
            assignments=(AssignmentColEq(left="city", right="name"),),
            where=WhereEq(column="name", value=TextValue(value="Alice"))
        ))
        assert count == 1
        result = ex.select(SelectStmt(
            table="users",
            columns="*",
            where=WhereEq(column="name", value=TextValue(value="Alice"))
        ))
        assert result.rows[0][2] == TextValue(value="Alice")

    def test_update_all_rows(self, store: FileStorage) -> None:
        ex = _make_users_executor(store)
        count = ex.update(UpdateStmt(
            table="users",
            assignments=(Assignment(column="city", value=TextValue(value="SF")),),
            where=None
        ))
        assert count == 3
        result = ex.select(SelectStmt(table="users", columns="*", where=None))
        assert all(r[2] == TextValue(value="SF") for r in result.rows)

    def test_update_no_match(self, store: FileStorage) -> None:
        ex = _make_users_executor(store)
        original = ex.select(SelectStmt(table="users", columns="*", where=None))
        count = ex.update(UpdateStmt(
            table="users",
            assignments=(Assignment(column="city", value=TextValue(value="SF")),),
            where=WhereEq(column="name", value=TextValue(value="Nobody"))
        ))
        assert count == 0
        after = ex.select(SelectStmt(table="users", columns="*", where=None))
        assert original.rows == after.rows

    def test_update_multiple_columns(self, store: FileStorage) -> None:
        ex = _make_users_executor(store)
        count = ex.update(UpdateStmt(
            table="users",
            assignments=(
                Assignment(column="age", value=IntValue(value=99)),
                Assignment(column="city", value=TextValue(value="SF"))
            ),
            where=WhereEq(column="name", value=TextValue(value="Alice"))
        ))
        assert count == 1
        result = ex.select(SelectStmt(
            table="users",
            columns="*",
            where=WhereEq(column="name", value=TextValue(value="Alice"))
        ))
        assert result.rows[0] == (
            TextValue(value="Alice"),
            IntValue(value=99),
            TextValue(value="SF")
        )

    def test_update_mixed_assignments(self, store: FileStorage) -> None:
        ex = _make_users_executor(store)
        count = ex.update(UpdateStmt(
            table="users",
            assignments=(
                Assignment(column="city", value=TextValue(value="SF")),
                AssignmentColEq(left="city", right="name")
            ),
            where=WhereEq(column="name", value=TextValue(value="Alice"))
        ))
        assert count == 1
        result = ex.select(SelectStmt(
            table="users",
            columns="*",
            where=WhereEq(column="name", value=TextValue(value="Alice"))
        ))
        assert result.rows[0] == (
            TextValue(value="Alice"),
            IntValue(value=30),
            TextValue(value="Alice")
        )

    def test_update_swap_columns(self, executor: Executor) -> None:
        cols = (
            ColumnDef(name="a", type=ColumnType.TEXT),
            ColumnDef(name="b", type=ColumnType.TEXT),
        )
        executor.create_table(CreateTableStmt(name="t", columns=cols))
        executor.insert(InsertStmt(
            table="t",
            columns=("a", "b"),
            values=(TextValue(value="x"), TextValue(value="y"))
        ))
        executor.update(UpdateStmt(
            table="t",
            assignments=(
                AssignmentColEq(left="a", right="b"),
                AssignmentColEq(left="b", right="a")
            ),
            where=None
        ))
        result = executor.select(SelectStmt(table="t", columns="*", where=None))
        assert result.rows == ((TextValue(value="y"), TextValue(value="x")),)

    def test_update_where_matches_multiple(self, store: FileStorage) -> None:
        ex = _make_users_executor(store)
        count = ex.update(UpdateStmt(
            table="users",
            assignments=(Assignment(column="city", value=TextValue(value="Boston")),),
            where=WhereEq(column="city", value=TextValue(value="NYC"))
        ))
        assert count == 2
        result = ex.select(SelectStmt(table="users", columns="*", where=None))
        assert all(
            r[2] == TextValue(value="Boston")
            for r in result.rows
            if r[0] != TextValue(value="Bob")
        )
        bob = ex.select(SelectStmt(
            table="users", columns=("city",),
            where=WhereEq(column="name", value=TextValue(value="Bob"))
        ))
        assert bob.rows == ((TextValue(value="LA"),),)

    def test_update_nonexistent_column_in_assignments(self, store: FileStorage) -> None:
        ex = _make_users_executor(store)
        with pytest.raises(ColumnMismatchError):
            ex.update(UpdateStmt(
                table="users",
                assignments=(Assignment(column="zzz", value=TextValue(value="x")),),
                where=None
            ))

    def test_update_col_eq_nonexistent_column(self, store: FileStorage) -> None:
        ex = _make_users_executor(store)
        with pytest.raises(ColumnMismatchError):
            ex.update(UpdateStmt(
                table="users",
                assignments=(AssignmentColEq(left="city", right="zzz"),),
                where=None
            ))

    def test_table_not_found(self, executor: Executor) -> None:
        with pytest.raises(TableNotFoundError):
            executor.update(UpdateStmt(
                table="missing",
                assignments=(Assignment(column="a", value=TextValue(value="x")),),
                where=None
            ))

    def test_update_type_mismatch(self, store: FileStorage) -> None:
        cols = (_scd("a", StorageColumnType.INT),)
        store.create_table(TableName("t"), cols)
        store.insert_row(TableName("t"), (_si(1),))
        ex = Executor(store)
        with pytest.raises(TypeMismatchError) as exc_info:
            ex.update(UpdateStmt(
                table="t",
                assignments=(Assignment(column="a", value=TextValue(value="x")),),
                where=None
            ))
        assert exc_info.value.column == "a"

    def test_update_col_eq_type_mismatch(self, store: FileStorage) -> None:  
        cols = (
            _scd("a", StorageColumnType.INT),
            _scd("b", StorageColumnType.TEXT),
        )
        store.create_table(TableName("t"), cols)
        store.insert_row(TableName("t"), (_si(1), _st("x")))
        ex = Executor(store)
        with pytest.raises(TypeMismatchError) as exc_info:
            ex.update(UpdateStmt(
                table="t",
                assignments=(AssignmentColEq(left="a", right="b"),),
                where=None
            ))
        assert exc_info.value.column == "a"

    def test_update_same_value_still_counted(self, store: FileStorage) -> None:
        ex = _make_users_executor(store)
        original = ex.select(SelectStmt(table="users", columns="*", where=None))
        count = ex.update(UpdateStmt(
            table="users",
            assignments=(Assignment(column="city", value=TextValue(value="NYC")),),
            where=WhereEq(column="name", value=TextValue(value="Alice"))
        ))
        assert count == 1
        after = ex.select(SelectStmt(table="users", columns="*", where=None))
        assert original.rows == after.rows

    def test_update_with_where_col_eq(self, executor: Executor) -> None:
        cols = (
            ColumnDef(name="a", type=ColumnType.TEXT),
            ColumnDef(name="b", type=ColumnType.TEXT),
            ColumnDef(name="c", type=ColumnType.INT),
        )
        executor.create_table(CreateTableStmt(name="t", columns=cols))
        executor.insert(InsertStmt(table="t", columns=("a", "b", "c"),
            values=(TextValue(value="x"), TextValue(value="x"), IntValue(value=1))))
        executor.insert(InsertStmt(table="t", columns=("a", "b", "c"),
            values=(TextValue(value="x"), TextValue(value="y"), IntValue(value=2))))
        count = executor.update(UpdateStmt(
            table="t",
            assignments=(Assignment(column="c", value=IntValue(value=99)),),
            where=WhereColEq(left="a", right="b"),
        ))
        assert count == 1
        result = executor.select(SelectStmt(
            table="t", columns="*",
            where=WhereEq(column="c", value=IntValue(value=99)),
        ))
        assert len(result.rows) == 1
        assert result.rows[0][0] == TextValue(value="x")
        assert result.rows[0][1] == TextValue(value="x")

    def test_update_with_where_and(self, executor: Executor) -> None:
        cols = (
            ColumnDef(name="name", type=ColumnType.TEXT),
            ColumnDef(name="age", type=ColumnType.INT),
            ColumnDef(name="city", type=ColumnType.TEXT),
        )
        executor.create_table(CreateTableStmt(name="t", columns=cols))
        executor.insert(InsertStmt(table="t", columns=("name", "age", "city"),
            values=(TextValue(value="Alice"), IntValue(value=30), TextValue(value="NYC"))))
        executor.insert(InsertStmt(table="t", columns=("name", "age", "city"),
            values=(TextValue(value="Bob"), IntValue(value=30), TextValue(value="LA"))))
        count = executor.update(UpdateStmt(
            table="t",
            assignments=(Assignment(column="city", value=TextValue(value="SF")),),
            where=WhereAnd(operands=(
                WhereEq(column="age", value=IntValue(value=30)),
                WhereEq(column="city", value=TextValue(value="LA")),
            )),
        ))
        assert count == 1
        result = executor.select(SelectStmt(
            table="t", columns="*",
            where=WhereEq(column="name", value=TextValue(value="Bob")),
        ))
        assert result.rows[0][2] == TextValue(value="SF")

    def test_update_with_where_or(self, executor: Executor) -> None:
        cols = (
            ColumnDef(name="name", type=ColumnType.TEXT),
            ColumnDef(name="age", type=ColumnType.INT),
        )
        executor.create_table(CreateTableStmt(name="t", columns=cols))
        executor.insert(InsertStmt(table="t", columns=("name", "age"),
            values=(TextValue(value="Alice"), IntValue(value=30))))
        executor.insert(InsertStmt(table="t", columns=("name", "age"),
            values=(TextValue(value="Bob"), IntValue(value=25))))
        executor.insert(InsertStmt(table="t", columns=("name", "age"),
            values=(TextValue(value="Carol"), IntValue(value=30))))
        count = executor.update(UpdateStmt(
            table="t",
            assignments=(Assignment(column="age", value=IntValue(value=99)),),
            where=WhereOr(operands=(
                WhereEq(column="name", value=TextValue(value="Alice")),
                WhereEq(column="name", value=TextValue(value="Carol")),
            )),
        ))
        assert count == 2
        result = executor.select(SelectStmt(
            table="t", columns="*",
            where=WhereEq(column="age", value=IntValue(value=99)),
        ))
        assert len(result.rows) == 2

    def test_update_self_assignment(self, executor: Executor) -> None:
        cols = (
            ColumnDef(name="a", type=ColumnType.TEXT),
            ColumnDef(name="b", type=ColumnType.INT),
        )
        executor.create_table(CreateTableStmt(name="t", columns=cols))
        executor.insert(InsertStmt(table="t", columns=("a", "b"),
            values=(TextValue(value="x"), IntValue(value=42))))
        count = executor.update(UpdateStmt(
            table="t",
            assignments=(AssignmentColEq(left="a", right="a"),),
            where=None,
        ))
        assert count == 1
        result = executor.select(SelectStmt(table="t", columns="*", where=None))
        assert result.rows == ((TextValue(value="x"), IntValue(value=42)),)


class TestDelete:
    def test_delete_with_where(self, store: FileStorage) -> None:
        ex = _make_users_executor(store)
        count = ex.delete(DeleteStmt(
            table="users",
            where=WhereEq(column="name", value=TextValue(value="Alice"))
        ))
        assert count == 1
        result = ex.select(SelectStmt(table="users", columns="*", where=None))
        assert len(result.rows) == 2
        remaining_names = {r[0] for r in result.rows}
        assert remaining_names == {TextValue(value="Bob"), TextValue(value="Carol")}

    def test_delete_all(self, store: FileStorage) -> None:
        ex = _make_users_executor(store)
        count = ex.delete(DeleteStmt(table="users", where=None))
        assert count == 3
        result = ex.select(SelectStmt(table="users", columns="*", where=None))
        assert result.rows == ()

    def test_delete_no_match(self, store: FileStorage) -> None:
        ex = _make_users_executor(store)
        original = ex.select(SelectStmt(table="users", columns="*", where=None))
        count = ex.delete(DeleteStmt(
            table="users",
            where=WhereEq(column="name", value=TextValue(value="Nobody"))
        ))
        assert count == 0
        after = ex.select(SelectStmt(table="users", columns="*", where=None))
        assert original.rows == after.rows

    def test_delete_then_select_deleted_value(self, store: FileStorage) -> None:
        ex = _make_users_executor(store)
        ex.delete(DeleteStmt(
            table="users",
            where=WhereEq(column="name", value=TextValue(value="Alice"))
        ))
        result = ex.select(SelectStmt(
            table="users",
            columns="*",
            where=WhereEq(column="name", value=TextValue(value="Alice"))
        ))
        assert result.rows == ()

    def test_table_not_found(self, executor: Executor) -> None:
        with pytest.raises(TableNotFoundError):
            executor.delete(DeleteStmt(table="missing", where=None))

    def test_delete_with_where_and(self, executor: Executor) -> None:
        cols = (
            ColumnDef(name="name", type=ColumnType.TEXT),
            ColumnDef(name="age", type=ColumnType.INT),
            ColumnDef(name="city", type=ColumnType.TEXT),
        )
        executor.create_table(CreateTableStmt(name="t", columns=cols))
        executor.insert(InsertStmt(table="t", columns=("name", "age", "city"),
            values=(TextValue(value="Alice"), IntValue(value=30), TextValue(value="NYC"))))
        executor.insert(InsertStmt(table="t", columns=("name", "age", "city"),
            values=(TextValue(value="Bob"), IntValue(value=30), TextValue(value="LA"))))
        executor.insert(InsertStmt(table="t", columns=("name", "age", "city"),
            values=(TextValue(value="Carol"), IntValue(value=25), TextValue(value="NYC"))))
        count = executor.delete(DeleteStmt(
            table="t",
            where=WhereAnd(operands=(
                WhereEq(column="age", value=IntValue(value=30)),
                WhereEq(column="city", value=TextValue(value="NYC")),
            ))
        ))
        assert count == 1
        result = executor.select(SelectStmt(table="t", columns="*", where=None))
        assert len(result.rows) == 2
        remaining_names = {r[0] for r in result.rows}
        assert remaining_names == {TextValue(value="Bob"), TextValue(value="Carol")}

    def test_delete_with_where_or(self, executor: Executor) -> None:
        cols = (
            ColumnDef(name="name", type=ColumnType.TEXT),
            ColumnDef(name="age", type=ColumnType.INT),
        )
        executor.create_table(CreateTableStmt(name="t", columns=cols))
        executor.insert(InsertStmt(table="t", columns=("name", "age"),
            values=(TextValue(value="Alice"), IntValue(value=30))))
        executor.insert(InsertStmt(table="t", columns=("name", "age"),
            values=(TextValue(value="Bob"), IntValue(value=25))))
        executor.insert(InsertStmt(table="t", columns=("name", "age"),
            values=(TextValue(value="Carol"), IntValue(value=30))))
        count = executor.delete(DeleteStmt(
            table="t",
            where=WhereOr(operands=(
                WhereEq(column="name", value=TextValue(value="Alice")),
                WhereEq(column="name", value=TextValue(value="Carol")),
            ))
        ))
        assert count == 2
        result = executor.select(SelectStmt(table="t", columns="*", where=None))
        assert len(result.rows) == 1
        assert result.rows[0][0] == TextValue(value="Bob")

    def test_delete_with_where_col_eq(self, executor: Executor) -> None:
        cols = (
            ColumnDef(name="a", type=ColumnType.TEXT),
            ColumnDef(name="b", type=ColumnType.TEXT),
        )
        executor.create_table(CreateTableStmt(name="t", columns=cols))
        executor.insert(InsertStmt(table="t", columns=("a", "b"),
            values=(TextValue(value="x"), TextValue(value="x"))))
        executor.insert(InsertStmt(table="t", columns=("a", "b"),
            values=(TextValue(value="x"), TextValue(value="y"))))
        count = executor.delete(DeleteStmt(
            table="t",
            where=WhereColEq(left="a", right="b"),
        ))
        assert count == 1
        result = executor.select(SelectStmt(table="t", columns="*", where=None))
        assert len(result.rows) == 1
        assert result.rows[0] == (TextValue(value="x"), TextValue(value="y"))


class TestLifecycleSequences:
    def test_insert_after_delete(self, executor: Executor) -> None:
        cols = (ColumnDef(name="a", type=ColumnType.TEXT),)
        executor.create_table(CreateTableStmt(name="t", columns=cols))
        executor.insert(InsertStmt(
            table="t",
            columns=("a",),
            values=(TextValue(value="x"),)
        ))
        executor.delete(DeleteStmt(table="t", where=None))
        executor.insert(InsertStmt(
            table="t",
            columns=("a",),
            values=(TextValue(value="y"),)
        ))
        result = executor.select(SelectStmt(table="t", columns="*", where=WhereEq(
            column="a",
            value=TextValue(value="y")
        )))
        assert len(result.rows) == 1

    def test_crud_cycle(self, executor: Executor) -> None:
        cols = (
            ColumnDef(name="a", type=ColumnType.TEXT),
            ColumnDef(name="b", type=ColumnType.INT),
        )
        executor.create_table(CreateTableStmt(name="t", columns=cols))
        executor.insert(InsertStmt(
            table="t",
            columns=("a", "b"),
            values=(TextValue(value="x"), IntValue(value=42))
        ))
        result = executor.select(SelectStmt(table="t", columns="*", where=None))
        assert result.rows == ((TextValue(value="x"), IntValue(value=42)),)

        executor.update(UpdateStmt(
            table="t",
            assignments=(Assignment(column="b", value=IntValue(value=99)),),
            where=WhereEq(column="a", value=TextValue(value="x"))
        ))
        result = executor.select(SelectStmt(table="t", columns="*", where=None))
        assert result.rows == ((TextValue(value="x"), IntValue(value=99)),)

        executor.delete(DeleteStmt(
            table="t",
            where=WhereEq(column="a", value=TextValue(value="x"))
        ))
        result = executor.select(SelectStmt(table="t", columns="*", where=None))
        assert result.rows == ()

    def test_multi_row_mixed_operations(self, executor: Executor) -> None:
        cols = (
            ColumnDef(name="name", type=ColumnType.TEXT),
            ColumnDef(name="age", type=ColumnType.INT),
            ColumnDef(name="city", type=ColumnType.TEXT),
        )
        executor.create_table(CreateTableStmt(name="t", columns=cols))
        executor.insert(InsertStmt(
            table="t",
            columns=("name", "age", "city"),
            values=(TextValue(value="Alice"), IntValue(value=30), TextValue(value="NYC"))
        ))
        executor.insert(InsertStmt(
            table="t",
            columns=("name", "age", "city"),
            values=(TextValue(value="Bob"), IntValue(value=25), TextValue(value="LA"))
        ))
        executor.insert(InsertStmt(
            table="t",
            columns=("name", "age", "city"),
            values=(TextValue(value="Carol"), IntValue(value=30), TextValue(value="NYC"))
        ))

        executor.update(UpdateStmt(
            table="t",
            assignments=(Assignment(column="city", value=TextValue(value="SF")),),
            where=WhereEq(column="age", value=IntValue(value=30))
        ))
        result = executor.select(SelectStmt(
            table="t",
            columns="*",
            where=WhereEq(column="age", value=IntValue(value=30))
        ))
        assert all(r[2] == TextValue(value="SF") for r in result.rows)

        bob_result = executor.select(SelectStmt(
            table="t",
            columns="*",
            where=WhereEq(column="name", value=TextValue(value="Bob"))
        ))
        assert bob_result.rows[0][2] == TextValue(value="LA")

        executor.delete(DeleteStmt(
            table="t",
            where=WhereEq(column="city", value=TextValue(value="LA"))
        ))
        result = executor.select(SelectStmt(table="t", columns="*", where=None))
        assert len(result.rows) == 2

    def test_delete_then_reinsert(self, executor: Executor) -> None:
        cols = (
            ColumnDef(name="a", type=ColumnType.TEXT),
            ColumnDef(name="b", type=ColumnType.INT),
        )
        executor.create_table(CreateTableStmt(name="t", columns=cols))
        executor.insert(InsertStmt(
            table="t",
            columns=("a", "b"),
            values=(TextValue(value="x"), IntValue(value=42))
        ))
        executor.delete(DeleteStmt(table="t", where=None))
        executor.insert(InsertStmt(
            table="t",
            columns=("a", "b"),
            values=(TextValue(value="x"), IntValue(value=42))
        ))
        result = executor.select(SelectStmt(
            table="t",
            columns="*",
            where=WhereEq(column="a", value=TextValue(value="x"))
        ))
        assert len(result.rows) == 1

    def test_update_changing_where_column(self, store: FileStorage) -> None:
        ex = _make_users_executor(store)
        ex.update(UpdateStmt(
            table="users",
            assignments=(Assignment(column="name", value=TextValue(value="Zack")),),
            where=WhereEq(column="name", value=TextValue(value="Alice"))
        ))
        result = ex.select(SelectStmt(
            table="users",
            columns="*",
            where=WhereEq(column="name", value=TextValue(value="Alice"))
        ))
        assert len(result.rows) == 0
        result = ex.select(SelectStmt(
            table="users",
            columns="*",
            where=WhereEq(column="name", value=TextValue(value="Zack"))
        ))
        assert len(result.rows) == 1

    def test_sequential_updates_accumulate(self, store: FileStorage) -> None:
        cols = (
            _scd("name", StorageColumnType.TEXT),
            _scd("age", StorageColumnType.INT),
            _scd("city", StorageColumnType.TEXT),
        )
        store.create_table(TableName("users"), cols)
        store.insert_row(TableName("users"), (
            _st("Alice"),
            _si(30),
            _st("NYC")
        ))
        store.commit()
        ex = Executor(store)
        ex.update(UpdateStmt(
            table="users",
            assignments=(Assignment(column="city", value=TextValue(value="SF")),),
            where=WhereEq(column="name", value=TextValue(value="Alice"))
        ))
        ex.update(UpdateStmt(
            table="users",
            assignments=(Assignment(column="age", value=IntValue(value=99)),),
            where=WhereEq(column="name", value=TextValue(value="Alice"))
        ))
        result = ex.select(SelectStmt(
            table="users",
            columns="*",
            where=WhereEq(column="name", value=TextValue(value="Alice"))
        ))
        assert result.rows[0] == (
            TextValue(value="Alice"),
            IntValue(value=99),
            TextValue(value="SF")
        )

    def test_complex_nested_where_across_operations(self, executor: Executor) -> None:
        cols = (
            ColumnDef(name="name", type=ColumnType.TEXT),
            ColumnDef(name="age", type=ColumnType.INT),
            ColumnDef(name="city", type=ColumnType.TEXT),
        )
        executor.create_table(CreateTableStmt(name="t", columns=cols))
        executor.insert(InsertStmt(
            table="t",
            columns=("name", "age", "city"),
            values=(TextValue(value="Alice"), IntValue(value=30), TextValue(value="NYC"))
        ))
        executor.insert(InsertStmt(
            table="t",
            columns=("name", "age", "city"),
            values=(TextValue(value="Bob"), IntValue(value=25), TextValue(value="LA"))
        ))
        executor.insert(InsertStmt(
            table="t",
            columns=("name", "age", "city"),
            values=(TextValue(value="Carol"), IntValue(value=30), TextValue(value="SF"))
        ))

        where_or = WhereOr(operands=(
            WhereEq(column="name", value=TextValue(value="Alice")),
            WhereAnd(operands=(
                WhereEq(column="age", value=IntValue(value=30)),
                WhereEq(column="city", value=TextValue(value="SF"))
            ))
        ))
        result = executor.select(SelectStmt(table="t", columns="*", where=where_or))
        assert len(result.rows) == 2
        names = {r[0].value for r in result.rows}
        assert names == {"Alice", "Carol"}

        executor.update(UpdateStmt(
            table="t",
            assignments=(Assignment(column="age", value=IntValue(value=99)),),
            where=where_or
        ))
        result = executor.select(SelectStmt(
            table="t",
            columns="*",
            where=WhereEq(column="age", value=IntValue(value=99))
        ))
        assert len(result.rows) == 2

        executor.delete(DeleteStmt(
            table="t",
            where=WhereAnd(operands=(
                WhereEq(column="city", value=TextValue(value="NYC")),
                WhereEq(column="age", value=IntValue(value=99))
            ))
        ))
        result = executor.select(SelectStmt(table="t", columns="*", where=None))
        assert len(result.rows) == 2

    def test_failed_operation_leaves_state_unchanged(self, executor: Executor) -> None:
        cols = (
            ColumnDef(name="a", type=ColumnType.TEXT),
            ColumnDef(name="b", type=ColumnType.INT),
        )
        executor.create_table(CreateTableStmt(name="t", columns=cols))
        executor.insert(InsertStmt(
            table="t",
            columns=("a", "b"),
            values=(TextValue(value="x"), IntValue(value=42))
        ))
        original = executor.select(SelectStmt(table="t", columns="*", where=None))
        with pytest.raises(ColumnMismatchError):
            executor.select(SelectStmt(
                table="t",
                columns=("zzz",),
                where=None
            ))
        after = executor.select(SelectStmt(table="t", columns="*", where=None))
        assert original.rows == after.rows


class TestEqualitySemantics:

    def test_int_equality_filters(self, executor: Executor) -> None:
        cols = (ColumnDef(name="a", type=ColumnType.INT),)
        executor.create_table(CreateTableStmt(name="t", columns=cols))
        executor.insert(InsertStmt(table="t", columns=("a",), values=(IntValue(value=1),)))
        executor.insert(InsertStmt(table="t", columns=("a",), values=(IntValue(value=2),)))
        executor.insert(InsertStmt(table="t", columns=("a",), values=(IntValue(value=1),)))
        result = executor.select(SelectStmt(
            table="t", columns="*",
            where=WhereEq(column="a", value=IntValue(value=1))
        ))
        assert len(result.rows) == 2
        assert all(r[0] == IntValue(value=1) for r in result.rows)

    def test_bool_equality_filters(self, executor: Executor) -> None:
        cols = (ColumnDef(name="a", type=ColumnType.BOOL),)
        executor.create_table(CreateTableStmt(name="t", columns=cols))
        executor.insert(InsertStmt(table="t", columns=("a",), values=(BoolValue(value=True),)))
        executor.insert(InsertStmt(table="t", columns=("a",), values=(BoolValue(value=False),)))
        executor.insert(InsertStmt(table="t", columns=("a",), values=(BoolValue(value=True),)))
        result = executor.select(SelectStmt(
            table="t", columns="*",
            where=WhereEq(column="a", value=BoolValue(value=False))
        ))
        assert len(result.rows) == 1
        assert result.rows[0][0] == BoolValue(value=False)

    def test_text_equality_filters(self, executor: Executor) -> None:
        cols = (ColumnDef(name="a", type=ColumnType.TEXT),)
        executor.create_table(CreateTableStmt(name="t", columns=cols))
        executor.insert(InsertStmt(table="t", columns=("a",), values=(TextValue(value="hello"),)))
        executor.insert(InsertStmt(table="t", columns=("a",), values=(TextValue(value="world"),)))
        result = executor.select(SelectStmt(
            table="t", columns="*",
            where=WhereEq(column="a", value=TextValue(value="world"))
        ))
        assert len(result.rows) == 1
        assert result.rows[0][0] == TextValue(value="world")

    def test_cross_type_where_rejected_int_text(self, executor: Executor) -> None:
        cols = (ColumnDef(name="a", type=ColumnType.INT),)
        executor.create_table(CreateTableStmt(name="t", columns=cols))
        executor.insert(InsertStmt(table="t", columns=("a",), values=(IntValue(value=1),)))
        with pytest.raises(TypeMismatchError):
            executor.select(SelectStmt(
                table="t", columns="*",
                where=WhereEq(column="a", value=TextValue(value="1"))
            ))

    def test_cross_type_where_rejected_int_bool(self, executor: Executor) -> None:
        cols = (ColumnDef(name="a", type=ColumnType.INT),)
        executor.create_table(CreateTableStmt(name="t", columns=cols))
        executor.insert(InsertStmt(table="t", columns=("a",), values=(IntValue(value=1),)))
        with pytest.raises(TypeMismatchError):
            executor.select(SelectStmt(
                table="t", columns="*",
                where=WhereEq(column="a", value=BoolValue(value=True))
            ))

    def test_cross_type_where_rejected_bool_text(self, executor: Executor) -> None:
        cols = (ColumnDef(name="a", type=ColumnType.BOOL),)
        executor.create_table(CreateTableStmt(name="t", columns=cols))
        executor.insert(InsertStmt(table="t", columns=("a",), values=(BoolValue(value=True),)))
        with pytest.raises(TypeMismatchError):
            executor.select(SelectStmt(
                table="t", columns="*",
                where=WhereEq(column="a", value=TextValue(value="True"))
            ))

    def test_col_eq_rejects_cross_type(self, executor: Executor) -> None:
        cols = (
            ColumnDef(name="a", type=ColumnType.INT),
            ColumnDef(name="b", type=ColumnType.TEXT),
        )
        executor.create_table(CreateTableStmt(name="t", columns=cols))
        executor.insert(InsertStmt(
            table="t", columns=("a", "b"),
            values=(IntValue(value=1), TextValue(value="x"))
        ))
        with pytest.raises(TypeMismatchError):
            executor.select(SelectStmt(
                table="t", columns="*",
                where=WhereColEq(left="a", right="b")
            ))

    def test_col_eq_int_columns(self, executor: Executor) -> None:
        cols = (
            ColumnDef(name="a", type=ColumnType.INT),
            ColumnDef(name="b", type=ColumnType.INT),
        )
        executor.create_table(CreateTableStmt(name="t", columns=cols))
        executor.insert(InsertStmt(table="t", columns=("a", "b"),
            values=(IntValue(value=42), IntValue(value=42))))
        executor.insert(InsertStmt(table="t", columns=("a", "b"),
            values=(IntValue(value=42), IntValue(value=7))))
        result = executor.select(SelectStmt(
            table="t", columns="*",
            where=WhereColEq(left="a", right="b"),
        ))
        assert len(result.rows) == 1
        assert result.rows[0] == (IntValue(value=42), IntValue(value=42))

    def test_col_eq_bool_columns(self, executor: Executor) -> None:
        cols = (
            ColumnDef(name="a", type=ColumnType.BOOL),
            ColumnDef(name="b", type=ColumnType.BOOL),
        )
        executor.create_table(CreateTableStmt(name="t", columns=cols))
        executor.insert(InsertStmt(table="t", columns=("a", "b"),
            values=(BoolValue(value=True), BoolValue(value=True))))
        executor.insert(InsertStmt(table="t", columns=("a", "b"),
            values=(BoolValue(value=True), BoolValue(value=False))))
        result = executor.select(SelectStmt(
            table="t", columns="*",
            where=WhereColEq(left="a", right="b"),
        ))
        assert len(result.rows) == 1
        assert result.rows[0] == (BoolValue(value=True), BoolValue(value=True))


class TestMultipleTableIsolation:
    def _setup_two_tables(self, executor: Executor) -> None:
        users_cols = (
            ColumnDef(name="name", type=ColumnType.TEXT),
            ColumnDef(name="age", type=ColumnType.INT),
        )
        executor.create_table(CreateTableStmt(name="users", columns=users_cols))
        executor.insert(InsertStmt(table="users", columns=("name", "age"),
            values=(TextValue(value="Alice"), IntValue(value=30))))
        executor.insert(InsertStmt(table="users", columns=("name", "age"),
            values=(TextValue(value="Bob"), IntValue(value=25))))

        products_cols = (
            ColumnDef(name="item", type=ColumnType.TEXT),
            ColumnDef(name="price", type=ColumnType.INT),
        )
        executor.create_table(CreateTableStmt(name="products", columns=products_cols))
        executor.insert(InsertStmt(table="products", columns=("item", "price"),
            values=(TextValue(value="Widget"), IntValue(value=10))))
        executor.insert(InsertStmt(table="products", columns=("item", "price"),
            values=(TextValue(value="Gadget"), IntValue(value=20))))

    def test_delete_from_one_table_leaves_other_intact(self, executor: Executor) -> None:
        self._setup_two_tables(executor)
        executor.delete(DeleteStmt(
            table="users",
            where=WhereEq(column="name", value=TextValue(value="Alice")),
        ))
        users_result = executor.select(SelectStmt(table="users", columns="*", where=None))
        assert len(users_result.rows) == 1
        assert users_result.rows[0][0] == TextValue(value="Bob")
        products_result = executor.select(SelectStmt(table="products", columns="*", where=None))
        assert len(products_result.rows) == 2

    def test_delete_all_from_one_table_leaves_other_intact(self, executor: Executor) -> None:
        self._setup_two_tables(executor)
        executor.delete(DeleteStmt(table="users", where=None))
        assert executor.select(SelectStmt(table="users", columns="*", where=None)).rows == ()
        products_result = executor.select(SelectStmt(table="products", columns="*", where=None))
        assert len(products_result.rows) == 2

    def test_update_on_one_table_leaves_other_intact(self, executor: Executor) -> None:
        self._setup_two_tables(executor)
        executor.update(UpdateStmt(
            table="users",
            assignments=(Assignment(column="age", value=IntValue(value=99)),),
            where=None,
        ))
        users_result = executor.select(SelectStmt(table="users", columns="*", where=None))
        assert all(r[1] == IntValue(value=99) for r in users_result.rows)
        products_result = executor.select(SelectStmt(table="products", columns="*", where=None))
        assert products_result.rows[0][1] == IntValue(value=10)
        assert products_result.rows[1][1] == IntValue(value=20)

    def test_insert_into_one_table_leaves_other_unchanged(self, executor: Executor) -> None:
        self._setup_two_tables(executor)
        executor.insert(InsertStmt(table="users", columns=("name", "age"),
            values=(TextValue(value="Carol"), IntValue(value=35))))
        users_result = executor.select(SelectStmt(table="users", columns="*", where=None))
        assert len(users_result.rows) == 3
        products_result = executor.select(SelectStmt(table="products", columns="*", where=None))
        assert len(products_result.rows) == 2

    def test_select_does_not_cross_tables(self, executor: Executor) -> None:
        self._setup_two_tables(executor)
        users_result = executor.select(SelectStmt(table="users", columns="*", where=None))
        assert users_result.columns == ("name", "age")
        assert len(users_result.rows) == 2
        products_result = executor.select(SelectStmt(table="products", columns="*", where=None))
        assert products_result.columns == ("item", "price")
        assert len(products_result.rows) == 2

    def test_same_column_names_different_tables_isolated(self, executor: Executor) -> None:
        t1_cols = (
            ColumnDef(name="id", type=ColumnType.INT),
            ColumnDef(name="val", type=ColumnType.TEXT),
        )
        t2_cols = (
            ColumnDef(name="id", type=ColumnType.INT),
            ColumnDef(name="val", type=ColumnType.TEXT),
        )
        executor.create_table(CreateTableStmt(name="t1", columns=t1_cols))
        executor.create_table(CreateTableStmt(name="t2", columns=t2_cols))
        executor.insert(InsertStmt(table="t1", columns=("id", "val"),
            values=(IntValue(value=1), TextValue(value="a"))))
        executor.insert(InsertStmt(table="t2", columns=("id", "val"),
            values=(IntValue(value=1), TextValue(value="b"))))

        executor.update(UpdateStmt(
            table="t1",
            assignments=(Assignment(column="val", value=TextValue(value="changed")),),
            where=WhereEq(column="id", value=IntValue(value=1)),
        ))
        t1_result = executor.select(SelectStmt(table="t1", columns="*", where=None))
        assert t1_result.rows[0][1] == TextValue(value="changed")
        t2_result = executor.select(SelectStmt(table="t2", columns="*", where=None))
        assert t2_result.rows[0][1] == TextValue(value="b")

    def test_delete_from_one_table_then_insert_other_preserved(self, executor: Executor) -> None:
        self._setup_two_tables(executor)
        executor.delete(DeleteStmt(table="products", where=None))
        executor.insert(InsertStmt(table="users", columns=("name", "age"),
            values=(TextValue(value="Carol"), IntValue(value=35))))
        products_result = executor.select(SelectStmt(table="products", columns="*", where=None))
        assert products_result.rows == ()
        users_result = executor.select(SelectStmt(table="users", columns="*", where=None))
        assert len(users_result.rows) == 3
