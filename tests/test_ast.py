import pytest

from dbms.ast_nodes import (
    Assignment,
    AssignmentColEq,
    BoolValue,
    ColumnDef,
    ColumnType,
    CreateTableStmt,
    DeleteStmt,
    IntValue,
    InsertStmt,
    SelectStmt,
    TextValue,
    UpdateStmt,
    WhereAnd,
    WhereColEq,
    WhereEq,
    WhereOr,
    value_type,
)


class TestColumnType:
    def test_members(self) -> None:
        assert ColumnType.INT.value == "INT"
        assert ColumnType.BOOL.value == "BOOL"
        assert ColumnType.TEXT.value == "TEXT"


class TestColumnDef:
    def test_creation(self) -> None:
        cd = ColumnDef(name="id", type=ColumnType.INT)
        assert cd.name == "id"
        assert cd.type == ColumnType.INT

    def test_frozen(self) -> None:
        cd = ColumnDef(name="id", type=ColumnType.INT)
        with pytest.raises(AttributeError):
            cd.name = "other"  # type: ignore[misc]

    def test_equality(self) -> None:
        c1 = ColumnDef(name="id", type=ColumnType.INT)
        c2 = ColumnDef(name="id", type=ColumnType.INT)
        assert c1 == c2


class TestValueTypes:
    def test_int_value(self) -> None:
        v = IntValue(value=42)
        assert v.value == 42
        assert value_type(v) == ColumnType.INT

    def test_bool_value_true(self) -> None:
        v = BoolValue(value=True)
        assert v.value is True
        assert value_type(v) == ColumnType.BOOL

    def test_bool_value_false(self) -> None:
        v = BoolValue(value=False)
        assert v.value is False
        assert value_type(v) == ColumnType.BOOL

    def test_text_value(self) -> None:
        v = TextValue(value="hello")
        assert v.value == "hello"
        assert value_type(v) == ColumnType.TEXT

    def test_frozen_values(self) -> None:
        v = IntValue(value=42)
        with pytest.raises(AttributeError):
            v.value = 100  # type: ignore[misc]


class TestCreateTableStmt:
    def test_creation(self) -> None:
        cols = (ColumnDef(name="id", type=ColumnType.INT), ColumnDef(name="name", type=ColumnType.TEXT))
        stmt = CreateTableStmt(name="users", columns=cols)
        assert stmt.name == "users"
        assert len(stmt.columns) == 2
        assert stmt.columns[0].name == "id"
        assert stmt.columns[0].type == ColumnType.INT
        assert stmt.columns[1].name == "name"
        assert stmt.columns[1].type == ColumnType.TEXT

    def test_frozen(self) -> None:
        cols = (ColumnDef(name="a", type=ColumnType.INT),)
        stmt = CreateTableStmt(name="t", columns=cols)
        with pytest.raises(AttributeError):
            stmt.name = "other"  # type: ignore[misc]

    def test_equality(self) -> None:
        cols = (ColumnDef(name="a", type=ColumnType.INT),)
        s1 = CreateTableStmt(name="t", columns=cols)
        s2 = CreateTableStmt(name="t", columns=cols)
        assert s1 == s2


class TestInsertStmt:
    def test_creation(self) -> None:
        values = (IntValue(value=1), TextValue(value="Alice"))
        stmt = InsertStmt(table="users", columns=("id", "name"), value_rows=(values,))
        assert stmt.table == "users"
        assert stmt.columns == ("id", "name")
        assert len(stmt.value_rows) == 1
        assert len(stmt.value_rows[0]) == 2
        assert isinstance(stmt.value_rows[0][0], IntValue)
        assert isinstance(stmt.value_rows[0][1], TextValue)


class TestSelectStmt:
    def test_with_star(self) -> None:
        stmt = SelectStmt(table="users", columns="*", where=None)
        assert stmt.columns == "*"

    def test_with_columns(self) -> None:
        stmt = SelectStmt(table="users", columns=("name",), where=None)
        assert stmt.columns == ("name",)

    def test_with_where_eq(self) -> None:
        w = WhereEq(column="name", value=TextValue(value="Alice"))
        stmt = SelectStmt(table="users", columns="*", where=w)
        assert isinstance(stmt.where, WhereEq)
        assert stmt.where.column == "name"
        assert isinstance(stmt.where.value, TextValue)

    def test_with_where_and(self) -> None:
        w = WhereAnd(operands=(
            WhereEq(column="a", value=IntValue(value=1)),
            WhereEq(column="b", value=IntValue(value=2))
        ))
        stmt = SelectStmt(table="t", columns="*", where=w)
        assert isinstance(stmt.where, WhereAnd)
        assert len(stmt.where.operands) == 2

    def test_with_where_or(self) -> None:
        w = WhereOr(operands=(
            WhereEq(column="a", value=IntValue(value=1)),
            WhereEq(column="b", value=IntValue(value=2))
        ))
        stmt = SelectStmt(table="t", columns="*", where=w)
        assert isinstance(stmt.where, WhereOr)


class TestUpdateStmt:
    def test_creation(self) -> None:
        assignments = (Assignment(column="name", value=TextValue(value="Bob")),)
        where = WhereEq(column="id", value=IntValue(value=1))
        stmt = UpdateStmt(table="users", assignments=assignments, where=where)
        assert stmt.table == "users"
        assert len(stmt.assignments) == 1
        assert isinstance(stmt.where, WhereEq)

    def test_without_where(self) -> None:
        stmt = UpdateStmt(
            table="users",
            assignments=(Assignment(column="a", value=IntValue(value=1)),),
            where=None
        )
        assert stmt.where is None

    def test_assignment_col_eq(self) -> None:
        stmt = UpdateStmt(
            table="t",
            assignments=(AssignmentColEq(left="a", right="b"),),
            where=None
        )
        assert isinstance(stmt.assignments[0], AssignmentColEq)


class TestDeleteStmt:
    def test_with_where(self) -> None:
        where = WhereEq(column="name", value=TextValue(value="Alice"))
        stmt = DeleteStmt(table="users", where=where)
        assert isinstance(stmt.where, WhereEq)

    def test_without_where(self) -> None:
        stmt = DeleteStmt(table="users", where=None)
        assert stmt.where is None


class TestWhereEq:
    def test_creation(self) -> None:
        w = WhereEq(column="col", value=IntValue(value=42))
        assert w.column == "col"
        assert isinstance(w.value, IntValue)
        assert w.value.value == 42

    def test_frozen(self) -> None:
        w = WhereEq(column="col", value=IntValue(value=1))
        with pytest.raises(AttributeError):
            w.column = "other"  # type: ignore[misc]


class TestWhereAnd:
    def test_creation(self) -> None:
        w = WhereAnd(operands=(
            WhereEq(column="a", value=IntValue(value=1)),
            WhereEq(column="b", value=IntValue(value=2))
        ))
        assert len(w.operands) == 2

    def test_frozen(self) -> None:
        w = WhereAnd(operands=(WhereEq(column="a", value=IntValue(value=1)),))
        with pytest.raises(AttributeError):
            w.operands = ()  # type: ignore[misc]


class TestWhereOr:
    def test_creation(self) -> None:
        w = WhereOr(operands=(
            WhereEq(column="a", value=IntValue(value=1)),
            WhereEq(column="b", value=IntValue(value=2))
        ))
        assert len(w.operands) == 2

    def test_frozen(self) -> None:
        w = WhereOr(operands=(WhereEq(column="a", value=IntValue(value=1)),))
        with pytest.raises(AttributeError):
            w.operands = ()  # type: ignore[misc]


class TestAssignment:
    def test_creation(self) -> None:
        a = Assignment(column="col", value=IntValue(value=42))
        assert a.column == "col"
        assert isinstance(a.value, IntValue)

    def test_equality(self) -> None:
        a1 = Assignment(column="col", value=IntValue(value=42))
        a2 = Assignment(column="col", value=IntValue(value=42))
        assert a1 == a2


class TestValueTypeFunction:
    def test_int(self) -> None:
        assert value_type(IntValue(value=1)) == ColumnType.INT

    def test_bool(self) -> None:
        assert value_type(BoolValue(value=True)) == ColumnType.BOOL

    def test_text(self) -> None:
        assert value_type(TextValue(value="x")) == ColumnType.TEXT
