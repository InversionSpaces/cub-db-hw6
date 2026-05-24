import subprocess
from pathlib import Path

import pytest


@pytest.fixture
def db_file(tmp_path: Path) -> Path:
    return tmp_path / "test.db"


def run_cli(input_text: str, db_file: Path) -> tuple[str, int]:
    cmd = ["python", "main.py", str(db_file)]
    result = subprocess.run(
        cmd,
        input=input_text,
        capture_output=True,
        text=True,
        timeout=10,
    )
    return result.stdout, result.returncode


class TestCLIBasics:
    def test_help_command(self, db_file: Path) -> None:
        stdout, code = run_cli("help\nexit\n", db_file)
        assert code == 0
        assert "Commands:" in stdout
        assert "help" in stdout
        assert "exit" in stdout
        assert ".tables" in stdout
        assert "VACUUM" in stdout

    def test_exit_command(self, db_file: Path) -> None:
        stdout, code = run_cli("exit\n", db_file)
        assert code == 0
        assert "DBMS REPL" in stdout

    def test_quit_command(self, db_file: Path) -> None:
        stdout, code = run_cli("quit\n", db_file)
        assert code == 0
        assert "DBMS REPL" in stdout

    def test_backslash_q_command(self, db_file: Path) -> None:
        stdout, code = run_cli("\\q\n", db_file)
        assert code == 0
        assert "DBMS REPL" in stdout

    def test_empty_input(self, db_file: Path) -> None:
        stdout, code = run_cli("\n\nexit\n", db_file)
        assert code == 0
        assert "dbms>" in stdout

    def test_unknown_command_error(self, db_file: Path) -> None:
        stdout, code = run_cli("INVALID_SQL\nexit\n", db_file)
        assert code == 0
        assert "Error:" in stdout or "INVALID_SQL" in stdout


class TestCLITableOperations:
    def test_tables_empty(self, db_file: Path) -> None:
        stdout, code = run_cli(".tables\nexit\n", db_file)
        assert code == 0
        assert "No tables" in stdout

    def test_tables_with_data(self, db_file: Path) -> None:
        input_text = "CREATE TABLE users (name TEXT, age INT)\n.tables\nexit\n"
        stdout, code = run_cli(input_text, db_file)
        assert code == 0
        assert "users" in stdout
        assert "name TEXT" in stdout
        assert "age INT" in stdout

    def test_tables_case_insensitive(self, db_file: Path) -> None:
        input_text = "CREATE TABLE users (name TEXT)\ntables\nexit\n"
        stdout, code = run_cli(input_text, db_file)
        assert code == 0
        assert "users" in stdout


class TestCLICreateTable:
    def test_create_table_simple(self, db_file: Path) -> None:
        input_text = "CREATE TABLE users (name TEXT, age INT)\nexit\n"
        stdout, code = run_cli(input_text, db_file)
        assert code == 0
        assert "OK" in stdout

    def test_create_table_single_column(self, db_file: Path) -> None:
        input_text = "CREATE TABLE users (name TEXT)\nexit\n"
        stdout, code = run_cli(input_text, db_file)
        assert code == 0
        assert "OK" in stdout

    def test_create_multiple_tables(self, db_file: Path) -> None:
        input_text = "CREATE TABLE users (name TEXT)\nCREATE TABLE posts (title TEXT)\n.tables\nexit\n"
        stdout, code = run_cli(input_text, db_file)
        assert code == 0
        assert "users" in stdout
        assert "posts" in stdout

    def test_create_duplicate_table_error(self, db_file: Path) -> None:
        input_text = "CREATE TABLE users (name TEXT)\nCREATE TABLE users (age INT)\nexit\n"
        stdout, code = run_cli(input_text, db_file)
        assert code == 0
        assert "Error:" in stdout

    def test_tables_shows_all_column_types(self, db_file: Path) -> None:
        input_text = "CREATE TABLE users (id INT, name TEXT, active BOOL)\n.tables\nexit\n"
        stdout, code = run_cli(input_text, db_file)
        assert code == 0
        assert "id INT" in stdout
        assert "name TEXT" in stdout
        assert "active BOOL" in stdout


class TestCLIInsert:
    def test_insert_single_row(self, db_file: Path) -> None:
        input_text = "CREATE TABLE users (name TEXT, age INT)\nINSERT INTO users (name, age) VALUES ('Alice', 30)\nexit\n"
        stdout, code = run_cli(input_text, db_file)
        assert code == 0
        assert "Affected rows: 1" in stdout

    def test_insert_multiple_rows(self, db_file: Path) -> None:
        input_text = (
            "CREATE TABLE users (name TEXT, age INT)\n"
            "INSERT INTO users (name, age) VALUES ('Alice', 30)\n"
            "INSERT INTO users (name, age) VALUES ('Bob', 25)\n"
            "INSERT INTO users (name, age) VALUES ('Carol', 35)\n"
            "exit\n"
        )
        stdout, code = run_cli(input_text, db_file)
        assert code == 0
        assert stdout.count("Affected rows: 1") == 3

    def test_insert_with_escaped_quotes(self, db_file: Path) -> None:
        input_text = "CREATE TABLE users (name TEXT)\nINSERT INTO users (name) VALUES ('it''s')\nexit\n"
        stdout, code = run_cli(input_text, db_file)
        assert code == 0
        assert "Affected rows: 1" in stdout

    def test_insert_column_reorder(self, db_file: Path) -> None:
        input_text = "CREATE TABLE users (name TEXT, age INT)\nINSERT INTO users (age, name) VALUES (30, 'Alice')\nexit\n"
        stdout, code = run_cli(input_text, db_file)
        assert code == 0
        assert "Affected rows: 1" in stdout

    def test_insert_bool_value_true(self, db_file: Path) -> None:
        input_text = "CREATE TABLE users (id INT, active BOOL)\nINSERT INTO users (id, active) VALUES (1, TRUE)\nexit\n"
        stdout, code = run_cli(input_text, db_file)
        assert code == 0
        assert "Affected rows: 1" in stdout

    def test_insert_bool_value_false(self, db_file: Path) -> None:
        input_text = "CREATE TABLE users (id INT, active BOOL)\nINSERT INTO users (id, active) VALUES (1, FALSE)\nexit\n"
        stdout, code = run_cli(input_text, db_file)
        assert code == 0
        assert "Affected rows: 1" in stdout

    def test_insert_negative_int(self, db_file: Path) -> None:
        input_text = "CREATE TABLE users (id INT)\nINSERT INTO users (id) VALUES (-123)\nexit\n"
        stdout, code = run_cli(input_text, db_file)
        assert code == 0
        assert "Affected rows: 1" in stdout


class TestCLISelect:
    def test_select_empty_table(self, db_file: Path) -> None:
        input_text = "CREATE TABLE users (name TEXT)\nSELECT * FROM users\nexit\n"
        stdout, code = run_cli(input_text, db_file)
        assert code == 0
        assert "No rows" in stdout

    def test_select_all_columns(self, db_file: Path) -> None:
        input_text = (
            "CREATE TABLE users (name TEXT, age INT)\n"
            "INSERT INTO users (name, age) VALUES ('Alice', 30)\n"
            "SELECT * FROM users\n"
            "exit\n"
        )
        stdout, code = run_cli(input_text, db_file)
        assert code == 0
        assert "Alice" in stdout
        assert "30" in stdout

    def test_select_specific_columns(self, db_file: Path) -> None:
        input_text = (
            "CREATE TABLE users (name TEXT, age INT, city TEXT)\n"
            "INSERT INTO users (name, age, city) VALUES ('Alice', 30, 'NYC')\n"
            "SELECT name, city FROM users\n"
            "exit\n"
        )
        stdout, code = run_cli(input_text, db_file)
        assert code == 0
        assert "name" in stdout
        assert "city" in stdout
        assert "Alice" in stdout
        assert "NYC" in stdout

    def test_select_with_where(self, db_file: Path) -> None:
        input_text = (
            "CREATE TABLE users (name TEXT, age INT)\n"
            "INSERT INTO users (name, age) VALUES ('Alice', 30)\n"
            "INSERT INTO users (name, age) VALUES ('Bob', 25)\n"
            "SELECT * FROM users WHERE name = 'Alice'\n"
            "exit\n"
        )
        stdout, code = run_cli(input_text, db_file)
        assert code == 0
        assert "Alice" in stdout
        select_idx = stdout.rfind("name")
        exit_idx = stdout.rfind("exit")
        result_section = stdout[select_idx:exit_idx] if exit_idx > 0 else stdout[select_idx:]
        assert "Bob" not in result_section

    def test_select_multiple_rows(self, db_file: Path) -> None:
        input_text = (
            "CREATE TABLE users (name TEXT)\n"
            "INSERT INTO users (name) VALUES ('Alice')\n"
            "INSERT INTO users (name) VALUES ('Bob')\n"
            "SELECT * FROM users\n"
            "exit\n"
        )
        stdout, code = run_cli(input_text, db_file)
        assert code == 0
        assert "Alice" in stdout
        assert "Bob" in stdout

    def test_select_bool_values(self, db_file: Path) -> None:
        input_text = (
            "CREATE TABLE users (id INT, active BOOL)\n"
            "INSERT INTO users (id, active) VALUES (1, TRUE)\n"
            "INSERT INTO users (id, active) VALUES (2, FALSE)\n"
            "SELECT * FROM users\n"
            "exit\n"
        )
        stdout, code = run_cli(input_text, db_file)
        assert code == 0
        assert "TRUE" in stdout
        assert "FALSE" in stdout


class TestCLIUpdate:
    def test_update_single_row(self, db_file: Path) -> None:
        input_text = (
            "CREATE TABLE users (name TEXT, age INT)\n"
            "INSERT INTO users (name, age) VALUES ('Alice', 30)\n"
            "UPDATE users SET age = 31\n"
            "SELECT * FROM users\n"
            "exit\n"
        )
        stdout, code = run_cli(input_text, db_file)
        assert code == 0
        assert "Affected rows: 1" in stdout
        assert "31" in stdout

    def test_update_with_where(self, db_file: Path) -> None:
        input_text = (
            "CREATE TABLE users (name TEXT, age INT)\n"
            "INSERT INTO users (name, age) VALUES ('Alice', 30)\n"
            "INSERT INTO users (name, age) VALUES ('Bob', 25)\n"
            "UPDATE users SET age = 99 WHERE name = 'Alice'\n"
            "SELECT * FROM users\n"
            "exit\n"
        )
        stdout, code = run_cli(input_text, db_file)
        assert code == 0
        assert "Affected rows: 1" in stdout

    def test_update_multiple_columns(self, db_file: Path) -> None:
        input_text = (
            "CREATE TABLE users (name TEXT, age INT, city TEXT)\n"
            "INSERT INTO users (name, age, city) VALUES ('Alice', 30, 'NYC')\n"
            "UPDATE users SET age = 31, city = 'LA'\n"
            "SELECT * FROM users\n"
            "exit\n"
        )
        stdout, code = run_cli(input_text, db_file)
        assert code == 0
        assert "Affected rows: 1" in stdout
        assert "31" in stdout
        assert "LA" in stdout

    def test_update_bool_value(self, db_file: Path) -> None:
        input_text = (
            "CREATE TABLE users (id INT, active BOOL)\n"
            "INSERT INTO users (id, active) VALUES (1, FALSE)\n"
            "UPDATE users SET active = TRUE WHERE id = 1\n"
            "SELECT * FROM users\n"
            "exit\n"
        )
        stdout, code = run_cli(input_text, db_file)
        assert code == 0
        assert "Affected rows: 1" in stdout
        assert "TRUE" in stdout


class TestCLIDelete:
    def test_delete_all_rows(self, db_file: Path) -> None:
        input_text = (
            "CREATE TABLE users (name TEXT)\n"
            "INSERT INTO users (name) VALUES ('Alice')\n"
            "INSERT INTO users (name) VALUES ('Bob')\n"
            "DELETE FROM users\n"
            "SELECT * FROM users\n"
            "exit\n"
        )
        stdout, code = run_cli(input_text, db_file)
        assert code == 0
        assert "Affected rows: 2" in stdout
        assert "No rows" in stdout

    def test_delete_with_where(self, db_file: Path) -> None:
        input_text = (
            "CREATE TABLE users (name TEXT, age INT)\n"
            "INSERT INTO users (name, age) VALUES ('Alice', 30)\n"
            "INSERT INTO users (name, age) VALUES ('Bob', 25)\n"
            "DELETE FROM users WHERE name = 'Alice'\n"
            "SELECT * FROM users\n"
            "exit\n"
        )
        stdout, code = run_cli(input_text, db_file)
        assert code == 0
        assert "Affected rows: 1" in stdout
        assert "Bob" in stdout


class TestCLIVacuum:
    def test_vacuum_empty(self, db_file: Path) -> None:
        input_text = "VACUUM\nexit\n"
        stdout, code = run_cli(input_text, db_file)
        assert code == 0
        assert "OK" in stdout

    def test_vacuum_with_data(self, db_file: Path) -> None:
        input_text = (
            "CREATE TABLE users (name TEXT)\n"
            "INSERT INTO users (name) VALUES ('Alice')\n"
            "VACUUM\n"
            "exit\n"
        )
        stdout, code = run_cli(input_text, db_file)
        assert code == 0
        assert stdout.count("OK") >= 1


class TestCLIWhereExpressions:
    def test_where_and(self, db_file: Path) -> None:
        input_text = (
            "CREATE TABLE users (name TEXT, age INT, city TEXT)\n"
            "INSERT INTO users (name, age, city) VALUES ('Alice', 30, 'NYC')\n"
            "INSERT INTO users (name, age, city) VALUES ('Bob', 30, 'LA')\n"
            "INSERT INTO users (name, age, city) VALUES ('Carol', 25, 'NYC')\n"
            "SELECT * FROM users WHERE age = 30 AND city = 'NYC'\n"
            "exit\n"
        )
        stdout, code = run_cli(input_text, db_file)
        assert code == 0
        assert "Alice" in stdout

    def test_where_or(self, db_file: Path) -> None:
        input_text = (
            "CREATE TABLE users (name TEXT, age INT)\n"
            "INSERT INTO users (name, age) VALUES ('Alice', 30)\n"
            "INSERT INTO users (name, age) VALUES ('Bob', 25)\n"
            "INSERT INTO users (name, age) VALUES ('Carol', 30)\n"
            "SELECT * FROM users WHERE name = 'Alice' OR name = 'Carol'\n"
            "exit\n"
        )
        stdout, code = run_cli(input_text, db_file)
        assert code == 0
        assert "Alice" in stdout
        assert "Carol" in stdout

    def test_where_parentheses(self, db_file: Path) -> None:
        input_text = (
            "CREATE TABLE users (name TEXT, age INT, active BOOL)\n"
            "INSERT INTO users (name, age, active) VALUES ('Alice', 30, TRUE)\n"
            "INSERT INTO users (name, age, active) VALUES ('Bob', 25, FALSE)\n"
            "INSERT INTO users (name, age, active) VALUES ('Carol', 30, FALSE)\n"
            "SELECT * FROM users WHERE (age = 30 OR active = TRUE) AND name = 'Alice'\n"
            "exit\n"
        )
        stdout, code = run_cli(input_text, db_file)
        assert code == 0
        assert "Alice" in stdout

    def test_where_int_comparison(self, db_file: Path) -> None:
        input_text = (
            "CREATE TABLE users (name TEXT, age INT)\n"
            "INSERT INTO users (name, age) VALUES ('Alice', 30)\n"
            "INSERT INTO users (name, age) VALUES ('Bob', 25)\n"
            "SELECT * FROM users WHERE age = 30\n"
            "exit\n"
        )
        stdout, code = run_cli(input_text, db_file)
        assert code == 0
        assert "Alice" in stdout
        assert "Bob" not in stdout

    def test_where_bool_comparison(self, db_file: Path) -> None:
        input_text = (
            "CREATE TABLE users (name TEXT, active BOOL)\n"
            "INSERT INTO users (name, active) VALUES ('Alice', TRUE)\n"
            "INSERT INTO users (name, active) VALUES ('Bob', FALSE)\n"
            "SELECT * FROM users WHERE active = TRUE\n"
            "exit\n"
        )
        stdout, code = run_cli(input_text, db_file)
        assert code == 0
        assert "Alice" in stdout
        assert "Bob" not in stdout


class TestCLISessionPersistence:
    def test_data_persists_across_sessions(self, db_file: Path) -> None:
        input_text = "CREATE TABLE users (name TEXT)\nINSERT INTO users (name) VALUES ('Alice')\nexit\n"
        stdout, code = run_cli(input_text, db_file)
        assert code == 0

        input_text = "SELECT * FROM users\nexit\n"
        stdout, code = run_cli(input_text, db_file)
        assert code == 0
        assert "Alice" in stdout

    def test_tables_persist_across_sessions(self, db_file: Path) -> None:
        input_text = "CREATE TABLE users (name TEXT)\nexit\n"
        stdout, code = run_cli(input_text, db_file)
        assert code == 0

        input_text = ".tables\nexit\n"
        stdout, code = run_cli(input_text, db_file)
        assert code == 0
        assert "users" in stdout


class TestCLIErrorHandling:
    def test_table_not_found_error(self, db_file: Path) -> None:
        input_text = "SELECT * FROM nonexistent\nexit\n"
        stdout, code = run_cli(input_text, db_file)
        assert code == 0
        assert "Error:" in stdout

    def test_insert_into_nonexistent_table(self, db_file: Path) -> None:
        input_text = "INSERT INTO nonexistent (a TEXT) VALUES ('x')\nexit\n"
        stdout, code = run_cli(input_text, db_file)
        assert code == 0
        assert "Error:" in stdout

    def test_select_nonexistent_column(self, db_file: Path) -> None:
        input_text = "CREATE TABLE users (name TEXT)\nSELECT nonexistent FROM users\nexit\n"
        stdout, code = run_cli(input_text, db_file)
        assert code == 0
        assert "Error:" in stdout

    def test_type_mismatch_error(self, db_file: Path) -> None:
        input_text = "CREATE TABLE users (id INT)\nINSERT INTO users (id) VALUES ('not_an_int')\nexit\n"
        stdout, code = run_cli(input_text, db_file)
        assert code == 0
        assert "Error:" in stdout


class TestCLIComplexScenarios:
    def test_create_insert_select_update_delete_sequence(self, db_file: Path) -> None:
        input_text = (
            "CREATE TABLE products (id INT, name TEXT, price INT)\n"
            "INSERT INTO products (id, name, price) VALUES (1, 'Laptop', 1000)\n"
            "INSERT INTO products (id, name, price) VALUES (2, 'Phone', 500)\n"
            "SELECT * FROM products\n"
            "UPDATE products SET price = 800 WHERE id = 1\n"
            "DELETE FROM products WHERE id = 2\n"
            "SELECT * FROM products\n"
            "exit\n"
        )
        stdout, code = run_cli(input_text, db_file)
        assert code == 0
        assert "Laptop" in stdout
        assert "Phone" in stdout
        assert "Affected rows: 1" in stdout
        assert "800" in stdout

    def test_multiple_tables_join_like_operations(self, db_file: Path) -> None:
        input_text = (
            "CREATE TABLE users (id INT, name TEXT)\n"
            "CREATE TABLE orders (user_id INT, amount INT)\n"
            "INSERT INTO users (id, name) VALUES (1, 'Alice')\n"
            "INSERT INTO users (id, name) VALUES (2, 'Bob')\n"
            "INSERT INTO orders (user_id, amount) VALUES (1, 100)\n"
            "INSERT INTO orders (user_id, amount) VALUES (1, 200)\n"
            "INSERT INTO orders (user_id, amount) VALUES (2, 50)\n"
            "SELECT * FROM users\n"
            "SELECT * FROM orders WHERE user_id = 1\n"
            "exit\n"
        )
        stdout, code = run_cli(input_text, db_file)
        assert code == 0
        assert "Alice" in stdout
        assert "Bob" in stdout
        assert stdout.count("100") >= 1
        assert stdout.count("200") >= 1

    def test_bulk_insert_then_filter(self, db_file: Path) -> None:
        input_text = (
            "CREATE TABLE numbers (value INT)\n"
            "INSERT INTO numbers (value) VALUES (1)\n"
            "INSERT INTO numbers (value) VALUES (2)\n"
            "INSERT INTO numbers (value) VALUES (3)\n"
            "INSERT INTO numbers (value) VALUES (4)\n"
            "INSERT INTO numbers (value) VALUES (5)\n"
            "SELECT * FROM numbers WHERE value > 3\n"
            "exit\n"
        )
        stdout, code = run_cli(input_text, db_file)
        assert code == 0
        assert "4" in stdout
        assert "5" in stdout

    def test_update_all_then_verify(self, db_file: Path) -> None:
        input_text = (
            "CREATE TABLE items (name TEXT, status TEXT)\n"
            "INSERT INTO items (name, status) VALUES ('A', 'pending')\n"
            "INSERT INTO items (name, status) VALUES ('B', 'pending')\n"
            "INSERT INTO items (name, status) VALUES ('C', 'pending')\n"
            "UPDATE items SET status = 'done'\n"
            "SELECT * FROM items\n"
            "exit\n"
        )
        stdout, code = run_cli(input_text, db_file)
        assert code == 0
        assert "Affected rows: 3" in stdout
        assert "done" in stdout
        result_section = stdout[stdout.rfind("name"):]
        assert "pending" not in result_section


class TestCLIEdgeCases:
    def test_empty_string_values(self, db_file: Path) -> None:
        input_text = "CREATE TABLE users (name TEXT)\nINSERT INTO users (name) VALUES ('')\nSELECT * FROM users\nexit\n"
        stdout, code = run_cli(input_text, db_file)
        assert code == 0
        assert "Affected rows: 1" in stdout

    def test_special_characters_in_values(self, db_file: Path) -> None:
        input_text = (
            "CREATE TABLE users (name TEXT)\n"
            "INSERT INTO users (name) VALUES ('hello world')\n"
            "INSERT INTO users (name) VALUES ('test@test.com')\n"
            "INSERT INTO users (name) VALUES ('123-456-7890')\n"
            "SELECT * FROM users\n"
            "exit\n"
        )
        stdout, code = run_cli(input_text, db_file)
        assert code == 0
        assert "hello world" in stdout
        assert "test@test.com" in stdout
        assert "123-456-7890" in stdout

    def test_unicode_values(self, db_file: Path) -> None:
        input_text = "CREATE TABLE users (name TEXT)\nINSERT INTO users (name) VALUES ('café')\nSELECT * FROM users\nexit\n"
        stdout, code = run_cli(input_text, db_file)
        assert code == 0
        assert "café" in stdout

    def test_long_values(self, db_file: Path) -> None:
        long_string = "x" * 100
        input_text = f"CREATE TABLE users (name TEXT)\nINSERT INTO users (name) VALUES ('{long_string}')\nSELECT * FROM users\nexit\n"
        stdout, code = run_cli(input_text, db_file)
        assert code == 0
        assert long_string in stdout

    def test_nested_parentheses_where(self, db_file: Path) -> None:
        input_text = (
            "CREATE TABLE users (a TEXT, b TEXT, c TEXT, d TEXT)\n"
            "INSERT INTO users (a, b, c, d) VALUES ('1', '2', '3', '4')\n"
            "INSERT INTO users (a, b, c, d) VALUES ('5', '6', '7', '8')\n"
            "SELECT * FROM users WHERE ((a = '1' AND b = '2') OR (c = '7' AND d = '8'))\n"
            "exit\n"
        )
        stdout, code = run_cli(input_text, db_file)
        assert code == 0
        assert "1" in stdout
        assert "8" in stdout

    def test_complex_and_or_precedence(self, db_file: Path) -> None:
        input_text = (
            "CREATE TABLE users (name TEXT, role TEXT, active BOOL)\n"
            "INSERT INTO users (name, role, active) VALUES ('Admin', 'user', TRUE)\n"
            "INSERT INTO users (name, role, active) VALUES ('Editor', 'admin', FALSE)\n"
            "INSERT INTO users (name, role, active) VALUES ('Viewer', 'user', TRUE)\n"
            "SELECT * FROM users WHERE role = 'user' OR role = 'admin' AND active = TRUE\n"
            "exit\n"
        )
        stdout, code = run_cli(input_text, db_file)
        assert code == 0
        assert "Admin" in stdout
        assert "Viewer" in stdout


class TestCLIWorkflows:
    def test_create_drop_recreate(self, db_file: Path) -> None:
        input_text = (
            "CREATE TABLE temp (id INT)\n"
            "INSERT INTO temp (id) VALUES (1)\n"
            "VACUUM\n"
            "CREATE TABLE temp2 (id INT)\n"
            "INSERT INTO temp2 (id) VALUES (2)\n"
            ".tables\n"
            "exit\n"
        )
        stdout, code = run_cli(input_text, db_file)
        assert code == 0
        assert "temp" in stdout
        assert "temp2" in stdout

    def test_batch_operations_across_tables(self, db_file: Path) -> None:
        input_text = (
            "CREATE TABLE table1 (col1 TEXT)\n"
            "CREATE TABLE table2 (col2 TEXT)\n"
            "CREATE TABLE table3 (col3 TEXT)\n"
            "INSERT INTO table1 (col1) VALUES ('a')\n"
            "INSERT INTO table2 (col2) VALUES ('b')\n"
            "INSERT INTO table3 (col3) VALUES ('c')\n"
            "SELECT * FROM table1\n"
            "SELECT * FROM table2\n"
            "SELECT * FROM table3\n"
            "exit\n"
        )
        stdout, code = run_cli(input_text, db_file)
        assert code == 0
        assert "a" in stdout
        assert "b" in stdout
        assert "c" in stdout

    def test_vacuum_after_deletions(self, db_file: Path) -> None:
        input_text = (
            "CREATE TABLE items (id INT)\n"
            "INSERT INTO items (id) VALUES (1)\n"
            "INSERT INTO items (id) VALUES (2)\n"
            "INSERT INTO items (id) VALUES (3)\n"
            "DELETE FROM items WHERE id = 2\n"
            "VACUUM\n"
            "SELECT * FROM items\n"
            "exit\n"
        )
        stdout, code = run_cli(input_text, db_file)
        assert code == 0
        assert "Affected rows: 1" in stdout
        assert "OK" in stdout
        assert "1" in stdout
        assert "3" in stdout


class TestCLIMixedOperations:
    def test_insert_select_update_delete_repeat(self, db_file: Path) -> None:
        input_text = (
            "CREATE TABLE cycle (state TEXT)\n"
            "INSERT INTO cycle (state) VALUES ('created')\n"
            "SELECT * FROM cycle\n"
            "UPDATE cycle SET state = 'updated'\n"
            "SELECT * FROM cycle\n"
            "DELETE FROM cycle\n"
            "SELECT * FROM cycle\n"
            "INSERT INTO cycle (state) VALUES ('final')\n"
            "SELECT * FROM cycle\n"
            "exit\n"
        )
        stdout, code = run_cli(input_text, db_file)
        assert code == 0
        assert "created" in stdout
        assert "updated" in stdout
        assert "No rows" in stdout
        assert "final" in stdout

    def test_multi_table_cascading_updates(self, db_file: Path) -> None:
        input_text = (
            "CREATE TABLE categories (id INT, name TEXT)\n"
            "CREATE TABLE products (id INT, cat_id INT, name TEXT)\n"
            "INSERT INTO categories (id, name) VALUES (1, 'Electronics')\n"
            "INSERT INTO categories (id, name) VALUES (2, 'Books')\n"
            "INSERT INTO products (id, cat_id, name) VALUES (101, 1, 'Laptop')\n"
            "INSERT INTO products (id, cat_id, name) VALUES (102, 1, 'Phone')\n"
            "INSERT INTO products (id, cat_id, name) VALUES (201, 2, 'Novel')\n"
            "UPDATE categories SET name = 'Gadgets' WHERE id = 1\n"
            "SELECT * FROM categories\n"
            "SELECT * FROM products WHERE cat_id = 1\n"
            "exit\n"
        )
        stdout, code = run_cli(input_text, db_file)
        assert code == 0
        assert "Affected rows: 1" in stdout
        assert "Gadgets" in stdout
        assert "Books" in stdout
        assert "Laptop" in stdout
        assert "Phone" in stdout


class TestCLILargeOperations:
    def test_bulk_insert_many_rows(self, db_file: Path) -> None:
        input_text = "CREATE TABLE big (n INT)\n"
        for i in range(50):
            input_text += f"INSERT INTO big (n) VALUES ({i})\n"
        input_text += "SELECT * FROM big\nexit\n"
        stdout, code = run_cli(input_text, db_file)
        assert code == 0
        assert stdout.count("Affected rows: 1") == 50

    def test_wide_table(self, db_file: Path) -> None:
        cols = ", ".join(f"col{i} TEXT" for i in range(20))
        vals = ", ".join(f"'{i}'" for i in range(20))
        input_text = f"CREATE TABLE wide ({cols})\nINSERT INTO wide ({', '.join(f'col{i}' for i in range(20))}) VALUES ({vals})\nSELECT * FROM wide\nexit\n"
        stdout, code = run_cli(input_text, db_file)
        assert code == 0
        assert "Affected rows: 1" in stdout
        for i in range(20):
            assert f"col{i}" in stdout

    def test_many_tables(self, db_file: Path) -> None:
        input_text = ""
        for i in range(20):
            input_text += f"CREATE TABLE t{i} (id INT)\n"
        input_text += ".tables\nexit\n"
        stdout, code = run_cli(input_text, db_file)
        assert code == 0
        for i in range(20):
            assert f"t{i}" in stdout
