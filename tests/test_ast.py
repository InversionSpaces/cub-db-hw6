import pytest

from dbms.ast_nodes import (
    Assignment,
    CreateTableStmt,
    DeleteStmt,
    InsertStmt,
    SelectStmt,
    UpdateStmt,
    WhereAnd,
    WhereEq,
    WhereOr,
)


class TestCreateTableStmt:
    def test_creation(self) -> None:
        stmt = CreateTableStmt(name="users", columns=("name", "age"))
        assert stmt.name == "users"
        assert stmt.columns == ("name", "age")

    def test_frozen(self) -> None:
        stmt = CreateTableStmt(name="users", columns=("name",))
        with pytest.raises(AttributeError):
            stmt.name = "other"  # type: ignore[misc]

    def test_equality(self) -> None:
        s1 = CreateTableStmt(name="users", columns=("a",))
        s2 = CreateTableStmt(name="users", columns=("a",))
        assert s1 == s2


class TestInsertStmt:
    def test_creation(self) -> None:
        stmt = InsertStmt(table="users", columns=("name",), values=("Alice",))
        assert stmt.table == "users"
        assert stmt.columns == ("name",)
        assert stmt.values == ("Alice",)


class TestSelectStmt:
    def test_with_star(self) -> None:
        stmt = SelectStmt(table="users", columns="*", where=None)
        assert stmt.columns == "*"

    def test_with_columns(self) -> None:
        stmt = SelectStmt(table="users", columns=("name",), where=None)
        assert stmt.columns == ("name",)

    def test_with_where_eq(self) -> None:
        w = WhereEq(column="name", value="Alice")
        stmt = SelectStmt(table="users", columns="*", where=w)
        assert isinstance(stmt.where, WhereEq)
        assert stmt.where.column == "name"

    def test_with_where_and(self) -> None:
        w = WhereAnd(operands=(WhereEq(column="a", value="1"), WhereEq(column="b", value="2")))
        stmt = SelectStmt(table="t", columns="*", where=w)
        assert isinstance(stmt.where, WhereAnd)
        assert len(stmt.where.operands) == 2

    def test_with_where_or(self) -> None:
        w = WhereOr(operands=(WhereEq(column="a", value="1"), WhereEq(column="b", value="2")))
        stmt = SelectStmt(table="t", columns="*", where=w)
        assert isinstance(stmt.where, WhereOr)


class TestUpdateStmt:
    def test_creation(self) -> None:
        assignments = (Assignment(column="name", value="Bob"),)
        where = WhereEq(column="id", value="1")
        stmt = UpdateStmt(table="users", assignments=assignments, where=where)
        assert stmt.table == "users"
        assert len(stmt.assignments) == 1
        assert isinstance(stmt.where, WhereEq)

    def test_without_where(self) -> None:
        stmt = UpdateStmt(table="users", assignments=(Assignment(column="a", value="b"),), where=None)
        assert stmt.where is None


class TestDeleteStmt:
    def test_with_where(self) -> None:
        where = WhereEq(column="name", value="Alice")
        stmt = DeleteStmt(table="users", where=where)
        assert isinstance(stmt.where, WhereEq)

    def test_without_where(self) -> None:
        stmt = DeleteStmt(table="users", where=None)
        assert stmt.where is None


class TestWhereEq:
    def test_creation(self) -> None:
        w = WhereEq(column="col", value="val")
        assert w.column == "col"
        assert w.value == "val"

    def test_frozen(self) -> None:
        w = WhereEq(column="col", value="val")
        with pytest.raises(AttributeError):
            w.column = "other"  # type: ignore[misc]


class TestWhereAnd:
    def test_creation(self) -> None:
        w = WhereAnd(operands=(WhereEq(column="a", value="1"), WhereEq(column="b", value="2")))
        assert len(w.operands) == 2

    def test_frozen(self) -> None:
        w = WhereAnd(operands=(WhereEq(column="a", value="1"),))
        with pytest.raises(AttributeError):
            w.operands = ()  # type: ignore[misc]


class TestWhereOr:
    def test_creation(self) -> None:
        w = WhereOr(operands=(WhereEq(column="a", value="1"), WhereEq(column="b", value="2")))
        assert len(w.operands) == 2

    def test_frozen(self) -> None:
        w = WhereOr(operands=(WhereEq(column="a", value="1"),))
        with pytest.raises(AttributeError):
            w.operands = ()  # type: ignore[misc]


class TestAssignment:
    def test_creation(self) -> None:
        a = Assignment(column="col", value="val")
        assert a.column == "col"
        assert a.value == "val"

    def test_equality(self) -> None:
        a1 = Assignment(column="col", value="val")
        a2 = Assignment(column="col", value="val")
        assert a1 == a2