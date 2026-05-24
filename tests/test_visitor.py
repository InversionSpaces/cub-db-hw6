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
)
from dbms.errors import IntegerOverflowError, ParseError
from dbms.visitor import parse


def eq(col: str, val: str) -> str:
    return f"{col} = '{val}'"


def and_expr(*parts: str) -> str:
    return " AND ".join(parts)


def or_expr(*parts: str) -> str:
    return " OR ".join(parts)


def paren(s: str) -> str:
    return f"({s})"


class TestCreateTable:
    def test_basic(self) -> None:
        stmt = parse("CREATE TABLE users (name TEXT, age INT)")
        assert isinstance(stmt, CreateTableStmt)
        assert stmt.name == "users"
        assert len(stmt.columns) == 2
        assert stmt.columns[0].name == "name"
        assert stmt.columns[0].type == ColumnType.TEXT
        assert stmt.columns[1].name == "age"
        assert stmt.columns[1].type == ColumnType.INT

    def test_single_column(self) -> None:
        stmt = parse("CREATE TABLE t (col1 INT)")
        assert isinstance(stmt, CreateTableStmt)
        assert stmt.columns == (ColumnDef(name="col1", type=ColumnType.INT),)

    def test_many_columns(self) -> None:
        stmt = parse("CREATE TABLE t (a INT, b BOOL, c TEXT, d INT, e BOOL)")
        assert isinstance(stmt, CreateTableStmt)
        assert len(stmt.columns) == 5
        assert stmt.columns[0].type == ColumnType.INT
        assert stmt.columns[1].type == ColumnType.BOOL
        assert stmt.columns[2].type == ColumnType.TEXT
        assert stmt.columns[3].type == ColumnType.INT
        assert stmt.columns[4].type == ColumnType.BOOL

    def test_bool_column(self) -> None:
        stmt = parse("CREATE TABLE t (active BOOL)")
        assert isinstance(stmt, CreateTableStmt)
        assert stmt.columns[0].type == ColumnType.BOOL


class TestInsert:
    def test_basic(self) -> None:
        stmt = parse("INSERT INTO users (name, age) VALUES ('Alice', 30)")
        assert isinstance(stmt, InsertStmt)
        assert stmt.table == "users"
        assert stmt.columns == ("name", "age")
        assert len(stmt.values) == 2
        assert isinstance(stmt.values[0], TextValue)
        assert stmt.values[0].value == "Alice"
        assert isinstance(stmt.values[1], IntValue)
        assert stmt.values[1].value == 30

    def test_single_value(self) -> None:
        stmt = parse("INSERT INTO t (col) VALUES ('val')")
        assert isinstance(stmt, InsertStmt)
        assert stmt.columns == ("col",)
        assert isinstance(stmt.values[0], TextValue)
        assert stmt.values[0].value == "val"

    def test_int_value(self) -> None:
        stmt = parse("INSERT INTO t (n) VALUES (42)")
        assert isinstance(stmt, InsertStmt)
        assert isinstance(stmt.values[0], IntValue)
        assert stmt.values[0].value == 42

    def test_bool_value_true(self) -> None:
        stmt = parse("INSERT INTO t (b) VALUES (TRUE)")
        assert isinstance(stmt, InsertStmt)
        assert isinstance(stmt.values[0], BoolValue)
        assert stmt.values[0].value is True

    def test_bool_value_false(self) -> None:
        stmt = parse("INSERT INTO t (b) VALUES (FALSE)")
        assert isinstance(stmt, InsertStmt)
        assert isinstance(stmt.values[0], BoolValue)
        assert stmt.values[0].value is False

    def test_negative_int(self) -> None:
        stmt = parse("INSERT INTO t (n) VALUES (-123)")
        assert isinstance(stmt, InsertStmt)
        assert isinstance(stmt.values[0], IntValue)
        assert stmt.values[0].value == -123

    def test_zero_int(self) -> None:
        stmt = parse("INSERT INTO t (n) VALUES (0)")
        assert isinstance(stmt, InsertStmt)
        assert isinstance(stmt.values[0], IntValue)
        assert stmt.values[0].value == 0

    def test_mixed_types(self) -> None:
        stmt = parse("INSERT INTO t (a, b, c) VALUES (1, TRUE, 'x')")
        assert isinstance(stmt, InsertStmt)
        assert isinstance(stmt.values[0], IntValue)
        assert isinstance(stmt.values[1], BoolValue)
        assert isinstance(stmt.values[2], TextValue)

    def test_escaped_quotes(self) -> None:
        stmt = parse("INSERT INTO t (col) VALUES ('it''s')")
        assert isinstance(stmt, InsertStmt)
        assert stmt.values[0].value == "it's"


class TestSelect:
    def test_select_all(self) -> None:
        stmt = parse("SELECT * FROM users")
        assert isinstance(stmt, SelectStmt)
        assert stmt.table == "users"
        assert stmt.columns == "*"
        assert stmt.where is None

    def test_select_columns(self) -> None:
        stmt = parse("SELECT name, age FROM users")
        assert isinstance(stmt, SelectStmt)
        assert stmt.columns == ("name", "age")

    def test_select_with_where_eq_text(self) -> None:
        stmt = parse("SELECT * FROM users WHERE name = 'Alice'")
        assert isinstance(stmt, SelectStmt)
        assert isinstance(stmt.where, WhereEq)
        assert stmt.where.column == "name"
        assert isinstance(stmt.where.value, TextValue)
        assert stmt.where.value.value == "Alice"

    def test_select_with_where_eq_int(self) -> None:
        stmt = parse("SELECT * FROM users WHERE age = 30")
        assert isinstance(stmt, SelectStmt)
        assert isinstance(stmt.where, WhereEq)
        assert stmt.where.column == "age"
        assert isinstance(stmt.where.value, IntValue)
        assert stmt.where.value.value == 30

    def test_select_with_where_eq_bool(self) -> None:
        stmt = parse("SELECT * FROM users WHERE active = TRUE")
        assert isinstance(stmt, SelectStmt)
        assert isinstance(stmt.where, WhereEq)
        assert isinstance(stmt.where.value, BoolValue)
        assert stmt.where.value.value is True

    def test_select_with_where_eq_false(self) -> None:
        stmt = parse("SELECT * FROM users WHERE active = FALSE")
        assert isinstance(stmt, SelectStmt)
        assert isinstance(stmt.where, WhereEq)
        assert isinstance(stmt.where.value, BoolValue)
        assert stmt.where.value.value is False

    def test_select_with_and(self) -> None:
        stmt = parse("SELECT * FROM t WHERE a = 1 AND b = 2")
        assert isinstance(stmt, SelectStmt)
        assert isinstance(stmt.where, WhereAnd)
        assert len(stmt.where.operands) == 2
        assert stmt.where.operands[0] == WhereEq(column="a", value=IntValue(value=1))
        assert stmt.where.operands[1] == WhereEq(column="b", value=IntValue(value=2))

    def test_select_with_or(self) -> None:
        stmt = parse("SELECT * FROM t WHERE a = 1 OR b = 2")
        assert isinstance(stmt, SelectStmt)
        assert isinstance(stmt.where, WhereOr)
        assert len(stmt.where.operands) == 2

    def test_and_binds_tighter_than_or(self) -> None:
        stmt = parse("SELECT * FROM t WHERE a = 1 AND b = 2 OR c = 3")
        assert isinstance(stmt, SelectStmt)
        assert isinstance(stmt.where, WhereOr)
        assert len(stmt.where.operands) == 2
        left = stmt.where.operands[0]
        assert isinstance(left, WhereAnd)
        assert left.operands[0] == WhereEq(column="a", value=IntValue(value=1))
        assert left.operands[1] == WhereEq(column="b", value=IntValue(value=2))
        assert stmt.where.operands[1] == WhereEq(column="c", value=IntValue(value=3))

    def test_parenthesized_or_with_and(self) -> None:
        stmt = parse("SELECT * FROM t WHERE (a = 1 OR b = 2) AND c = 3")
        assert isinstance(stmt, SelectStmt)
        assert isinstance(stmt.where, WhereAnd)
        assert len(stmt.where.operands) == 2
        left = stmt.where.operands[0]
        assert isinstance(left, WhereOr)
        assert left.operands[0] == WhereEq(column="a", value=IntValue(value=1))
        assert left.operands[1] == WhereEq(column="b", value=IntValue(value=2))
        assert stmt.where.operands[1] == WhereEq(column="c", value=IntValue(value=3))

    def test_multiple_and(self) -> None:
        stmt = parse("SELECT * FROM t WHERE a = 1 AND b = 2 AND c = 3")
        assert isinstance(stmt, SelectStmt)
        assert isinstance(stmt.where, WhereAnd)
        assert len(stmt.where.operands) == 3

    def test_multiple_or(self) -> None:
        stmt = parse("SELECT * FROM t WHERE a = 1 OR b = 2 OR c = 3")
        assert isinstance(stmt, SelectStmt)
        assert isinstance(stmt.where, WhereOr)
        assert len(stmt.where.operands) == 3


class TestWhereColEq:
    def test_simple_col_eq(self) -> None:
        stmt = parse("SELECT * FROM t WHERE id1 = id2")
        assert isinstance(stmt, SelectStmt)
        assert isinstance(stmt.where, WhereColEq)
        assert stmt.where.left == "id1"
        assert stmt.where.right == "id2"

    def test_col_eq_with_and(self) -> None:
        stmt = parse("SELECT * FROM t WHERE a = b AND c = 1")
        assert isinstance(stmt, SelectStmt)
        assert isinstance(stmt.where, WhereAnd)
        assert isinstance(stmt.where.operands[0], WhereColEq)
        assert stmt.where.operands[0].left == "a"
        assert stmt.where.operands[0].right == "b"
        assert isinstance(stmt.where.operands[1], WhereEq)
        assert stmt.where.operands[1].column == "c"
        assert stmt.where.operands[1].value == IntValue(value=1)

    def test_col_eq_with_or(self) -> None:
        stmt = parse("SELECT * FROM t WHERE a = 1 OR b = c")
        assert isinstance(stmt, SelectStmt)
        assert isinstance(stmt.where, WhereOr)
        assert isinstance(stmt.where.operands[0], WhereEq)
        assert isinstance(stmt.where.operands[1], WhereColEq)

    def test_col_eq_in_update(self) -> None:
        stmt = parse("UPDATE t SET a = 'x' WHERE id1 = id2")
        assert isinstance(stmt, UpdateStmt)
        assert isinstance(stmt.where, WhereColEq)
        assert stmt.where.left == "id1"
        assert stmt.where.right == "id2"

    def test_col_eq_in_delete(self) -> None:
        stmt = parse("DELETE FROM t WHERE a = b")
        assert isinstance(stmt, DeleteStmt)
        assert isinstance(stmt.where, WhereColEq)
        assert stmt.where.left == "a"
        assert stmt.where.right == "b"

    def test_col_eq_parenthesized(self) -> None:
        stmt = parse("SELECT * FROM t WHERE (a = b)")
        assert isinstance(stmt, SelectStmt)
        assert isinstance(stmt.where, WhereColEq)
        assert stmt.where.left == "a"
        assert stmt.where.right == "b"


class TestUpdate:
    def test_basic(self) -> None:
        stmt = parse("UPDATE users SET name = 'Bob' WHERE name = 'Alice'")
        assert isinstance(stmt, UpdateStmt)
        assert stmt.table == "users"
        assert len(stmt.assignments) == 1
        assert isinstance(stmt.assignments[0], Assignment)
        assert stmt.assignments[0].column == "name"
        assert isinstance(stmt.assignments[0].value, TextValue)
        assert stmt.assignments[0].value.value == "Bob"
        assert isinstance(stmt.where, WhereEq)
        assert stmt.where.column == "name"
        assert isinstance(stmt.where.value, TextValue)
        assert stmt.where.value.value == "Alice"

    def test_multiple_assignments(self) -> None:
        stmt = parse("UPDATE users SET name = 'Bob', age = 30 WHERE id = 1")
        assert isinstance(stmt, UpdateStmt)
        assert len(stmt.assignments) == 2
        assert stmt.assignments[0] == Assignment(column="name", value=TextValue(value="Bob"))
        assert stmt.assignments[1] == Assignment(column="age", value=IntValue(value=30))

    def test_update_without_where(self) -> None:
        stmt = parse("UPDATE users SET name = 'Bob'")
        assert isinstance(stmt, UpdateStmt)
        assert stmt.where is None

    def test_update_with_and_where(self) -> None:
        stmt = parse("UPDATE t SET a = 'x' WHERE b = 1 AND c = 2")
        assert isinstance(stmt, UpdateStmt)
        assert isinstance(stmt.where, WhereAnd)

    def test_update_set_col_eq_col(self) -> None:
        stmt = parse("UPDATE t SET a = b")
        assert isinstance(stmt, UpdateStmt)
        assert isinstance(stmt.assignments[0], AssignmentColEq)
        assert stmt.assignments[0].left == "a"
        assert stmt.assignments[0].right == "b"

    def test_update_mixed_assignments(self) -> None:
        stmt = parse("UPDATE t SET a = 'x', b = c")
        assert isinstance(stmt, UpdateStmt)
        assert len(stmt.assignments) == 2
        assert isinstance(stmt.assignments[0], Assignment)
        assert stmt.assignments[0].column == "a"
        assert stmt.assignments[0].value == TextValue(value="x")
        assert isinstance(stmt.assignments[1], AssignmentColEq)
        assert stmt.assignments[1].left == "b"
        assert stmt.assignments[1].right == "c"

    def test_update_bool_assignment(self) -> None:
        stmt = parse("UPDATE t SET active = TRUE WHERE id = 1")
        assert isinstance(stmt, UpdateStmt)
        assert isinstance(stmt.assignments[0], Assignment)
        assert isinstance(stmt.assignments[0].value, BoolValue)
        assert stmt.assignments[0].value.value is True


class TestDelete:
    def test_with_where(self) -> None:
        stmt = parse("DELETE FROM users WHERE name = 'Alice'")
        assert isinstance(stmt, DeleteStmt)
        assert stmt.table == "users"
        assert isinstance(stmt.where, WhereEq)
        assert stmt.where.column == "name"
        assert isinstance(stmt.where.value, TextValue)
        assert stmt.where.value.value == "Alice"

    def test_without_where(self) -> None:
        stmt = parse("DELETE FROM users")
        assert isinstance(stmt, DeleteStmt)
        assert stmt.where is None

    def test_with_or(self) -> None:
        stmt = parse("DELETE FROM t WHERE a = 1 OR b = 2")
        assert isinstance(stmt, DeleteStmt)
        assert isinstance(stmt.where, WhereOr)


class TestParseErrors:
    def test_invalid_sql(self) -> None:
        with pytest.raises(ParseError):
            parse("INVALID SQL")

    def test_incomplete_statement(self) -> None:
        with pytest.raises(ParseError):
            parse("CREATE TABLE")

    def test_missing_parentheses(self) -> None:
        with pytest.raises(ParseError):
            parse("CREATE TABLE users name TEXT, age INT")

    def test_create_missing_type(self) -> None:
        with pytest.raises(ParseError):
            parse("CREATE TABLE users (name)")

    def test_insert_wrong_values(self) -> None:
        with pytest.raises(ParseError):
            parse("INSERT INTO t (a) VALUES (not_a_string)")

    def test_empty_string(self) -> None:
        with pytest.raises(ParseError):
            parse("")

    def test_integer_overflow(self) -> None:
        with pytest.raises(IntegerOverflowError):
            parse("INSERT INTO t (n) VALUES (9999999999999999999)")

    def test_negative_integer_overflow(self) -> None:
        with pytest.raises(IntegerOverflowError):
            parse("INSERT INTO t (n) VALUES (-9999999999999999999)")

    def test_lowercase_true_not_keyword(self) -> None:
        with pytest.raises(ParseError):
            parse("INSERT INTO t (b) VALUES (true)")

    def test_lowercase_false_not_keyword(self) -> None:
        with pytest.raises(ParseError):
            parse("INSERT INTO t (b) VALUES (false)")

    def test_lowercase_int_not_type(self) -> None:
        with pytest.raises(ParseError):
            parse("CREATE TABLE t (a int)")


class TestASTNodeTypes:
    def test_create_table_frozen(self) -> None:
        cols = (ColumnDef(name="a", type=ColumnType.INT),)
        stmt = CreateTableStmt(name="t", columns=cols)
        with pytest.raises(AttributeError):
            stmt.name = "other"  # type: ignore[misc]

    def test_where_eq_frozen(self) -> None:
        w = WhereEq(column="a", value=IntValue(value=1))
        with pytest.raises(AttributeError):
            w.column = "c"  # type: ignore[misc]

    def test_assignment_frozen(self) -> None:
        a = Assignment(column="a", value=IntValue(value=1))
        with pytest.raises(AttributeError):
            a.column = "c"  # type: ignore[misc]

    def test_where_and_frozen(self) -> None:
        w = WhereAnd(operands=(WhereEq(column="a", value=IntValue(value=1)),))
        with pytest.raises(AttributeError):
            w.operands = ()  # type: ignore[misc]

    def test_where_or_frozen(self) -> None:
        w = WhereOr(operands=(WhereEq(column="a", value=IntValue(value=1)),))
        with pytest.raises(AttributeError):
            w.operands = ()  # type: ignore[misc]


class TestGeneratedChainedAnd:
    @pytest.mark.parametrize("n", range(1, 8))
    def test_n_way_and(self, n: int) -> None:
        cols = [f"c{i}" for i in range(n)]
        vals = [str(i) for i in range(n)]
        clauses = [f"{c} = '{v}'" for c, v in zip(cols, vals)]
        sql = f"SELECT * FROM t WHERE {and_expr(*clauses)}"
        stmt = parse(sql)
        assert isinstance(stmt, SelectStmt)
        if n == 1:
            assert isinstance(stmt.where, WhereEq)
            assert stmt.where.column == "c0"
        else:
            assert isinstance(stmt.where, WhereAnd)
            assert len(stmt.where.operands) == n
            for i, operand in enumerate(stmt.where.operands):
                assert isinstance(operand, WhereEq)
                assert operand.column == f"c{i}"
                assert operand.value.value == str(i)


class TestGeneratedChainedOr:
    @pytest.mark.parametrize("n", range(1, 8))
    def test_n_way_or(self, n: int) -> None:
        cols = [f"c{i}" for i in range(n)]
        vals = [str(i) for i in range(n)]
        clauses = [f"{c} = '{v}'" for c, v in zip(cols, vals)]
        sql = f"SELECT * FROM t WHERE {or_expr(*clauses)}"
        stmt = parse(sql)
        assert isinstance(stmt, SelectStmt)
        if n == 1:
            assert isinstance(stmt.where, WhereEq)
            assert stmt.where.column == "c0"
        else:
            assert isinstance(stmt.where, WhereOr)
            assert len(stmt.where.operands) == n
            for i, operand in enumerate(stmt.where.operands):
                assert isinstance(operand, WhereEq)
                assert operand.column == f"c{i}"
                assert operand.value.value == str(i)


class TestGeneratedNestedParentheses:
    def test_double_nested_parens(self) -> None:
        sql = "SELECT * FROM t WHERE ((a = '1'))"
        stmt = parse(sql)
        assert isinstance(stmt, SelectStmt)
        assert isinstance(stmt.where, WhereEq)
        assert stmt.where.column == "a"

    def test_triple_nested_parens(self) -> None:
        sql = "SELECT * FROM t WHERE (((a = '1' AND b = '2')))"
        stmt = parse(sql)
        assert isinstance(stmt, SelectStmt)
        assert isinstance(stmt.where, WhereAnd)
        assert len(stmt.where.operands) == 2

    @pytest.mark.parametrize("depth", range(1, 6))
    def test_paren_depth_roundtrip(self, depth: int) -> None:
        inner = "a = '1'"
        wrapped = inner
        for _ in range(depth):
            wrapped = paren(wrapped)
        sql = f"SELECT * FROM t WHERE {wrapped}"
        stmt = parse(sql)
        assert isinstance(stmt, SelectStmt)
        assert isinstance(stmt.where, WhereEq)
        assert stmt.where.column == "a"
        assert stmt.where.value.value == "1"


class TestGeneratedMixedPrecedence:
    def test_and_or_and(self) -> None:
        sql = "SELECT * FROM t WHERE a = 1 AND b = 2 OR c = 3 AND d = 4"
        stmt = parse(sql)
        assert isinstance(stmt, SelectStmt)
        assert isinstance(stmt.where, WhereOr)
        assert len(stmt.where.operands) == 2
        left = stmt.where.operands[0]
        right = stmt.where.operands[1]
        assert isinstance(left, WhereAnd)
        assert isinstance(right, WhereAnd)
        assert len(left.operands) == 2
        assert len(right.operands) == 2

    def test_or_and_or(self) -> None:
        sql = "SELECT * FROM t WHERE a = 1 OR b = 2 AND c = 3 OR d = 4"
        stmt = parse(sql)
        assert isinstance(stmt, SelectStmt)
        assert isinstance(stmt.where, WhereOr)
        assert len(stmt.where.operands) == 3
        mid = stmt.where.operands[1]
        assert isinstance(mid, WhereAnd)
        assert len(mid.operands) == 2

    def test_parens_override_precedence(self) -> None:
        sql = "SELECT * FROM t WHERE (a = 1 OR b = 2) AND (c = 3 OR d = 4)"
        stmt = parse(sql)
        assert isinstance(stmt, SelectStmt)
        assert isinstance(stmt.where, WhereAnd)
        assert len(stmt.where.operands) == 2
        assert isinstance(stmt.where.operands[0], WhereOr)
        assert isinstance(stmt.where.operands[1], WhereOr)

    def test_parens_inside_and(self) -> None:
        sql = "SELECT * FROM t WHERE a = 1 AND (b = 2 OR c = 3)"
        stmt = parse(sql)
        assert isinstance(stmt, SelectStmt)
        assert isinstance(stmt.where, WhereAnd)
        assert len(stmt.where.operands) == 2
        assert isinstance(stmt.where.operands[0], WhereEq)
        assert isinstance(stmt.where.operands[1], WhereOr)

    def test_nested_parens_with_and_or(self) -> None:
        sql = "SELECT * FROM t WHERE (a = 1 AND b = 2) OR (c = 3 AND (d = 4 OR e = 5))"
        stmt = parse(sql)
        assert isinstance(stmt, SelectStmt)
        assert isinstance(stmt.where, WhereOr)
        assert len(stmt.where.operands) == 2
        assert isinstance(stmt.where.operands[0], WhereAnd)
        assert isinstance(stmt.where.operands[1], WhereAnd)
        inner_and = stmt.where.operands[1]
        assert len(inner_and.operands) == 2
        assert isinstance(inner_and.operands[0], WhereEq)
        assert isinstance(inner_and.operands[1], WhereOr)
