# Simple File-Based DBMS

A Python file-based DBMS supporting multiple named tables with string-only columns.

## CLI Usage

Run the REPL with a database file:

```sh
uv run python main.py <database_file>
```

Example session:

```
$ uv run python main.py mydb.db
DBMS REPL. Database: mydb.db
Type 'exit' or 'quit' to exit.

dbms> CREATE TABLE users (name, age)
dbms> OK
dbms> INSERT INTO users (name, age) VALUES ('Alice', '30')
dbms> Affected rows: 1
dbms> SELECT * FROM users
dbms> name  | age
dbms> -----------
dbms> Alice | 30
dbms> 
```

### REPL Commands

| Command | Description |
|---------|-------------|
| `help` | Show help |
| `exit`, `quit`, `\q` | Exit the REPL |
| `.tables` | List all tables |
| `VACUUM` | Optimize database file |
| SQL statement | Execute SQL |

## SQL Syntax

```sql
CREATE TABLE <name> (<col>, ...)
INSERT INTO <name> (<col>, ...) VALUES (<val>, ...)
SELECT <col>, ... | * FROM <name> [WHERE <expr>]
UPDATE <name> SET <col> = <val>, ... [WHERE <expr>]
DELETE FROM <name> [WHERE <expr>]
```

WHERE expressions support `AND`, `OR`, and parenthesized grouping:

```sql
WHERE a = '1' AND b = '2' OR c = '3'
WHERE (a = '1' OR b = '2') AND c = '3'
```

All values are string literals using single quotes. Double single quotes to escape: `'it''s'`.

---

## Architecture

The system follows a layered design: SQL text is parsed into an immutable AST, which the executor interprets by calling storage operations.

### Storage Layer

The storage layer uses a **PostgreSQL-inspired slotted page format** with 4KB fixed-size pages. Each page contains a header, an array of item pointers, and the actual data items stored from the end of the page upward. Rows are limited to approximately 4KB in size.

Meta pages form a singly linked list starting from page 0. Each table's data pages form their own separate linked list. The metadata chain contains one entry per table with the table name, column names, and pointer to the head of that table's data page chain.

The system maintains an **LRU page cache** to avoid repeated disk I/O. Clean pages can be evicted when the cache fills, but dirty pages must remain in memory until commit. This means long transactions that modify many pages will accumulate memory pressure.

### Transaction Model

The system uses **statement-level auto-commit** where each SQL statement commits independently. Operations are first staged in memory, then applied to pages and persisted to disk with fsync for durability.

There is no support for concurrent access (single-writer model). Updates are performed in-place when the new row fits in the old slot, otherwise the old slot is deleted and the row inserted elsewhere. **Duplicate rows are allowed** as there are no uniqueness constraints (no PRIMARY KEY or UNIQUE support).

## Project Structure

```
hw6/
├── pyproject.toml
├── Makefile
├── main.py
├── grammar/
│   └── SimpleSQL.g4
├── src/dbms/
│   ├── __init__.py
│   ├── ast_nodes.py
│   ├── errors.py
│   ├── visitor.py
│   ├── in_memory_storage.py
│   ├── storage_protocol.py
│   ├── storage.py
│   ├── executor.py
│   └── generated/
│       ├── SimpleSQLLexer.py
│       ├── SimpleSQLParser.py
│       └── SimpleSQLVisitor.py
└── tests/
    ├── conftest.py
    ├── test_ast.py
    ├── test_visitor.py
    ├── test_executor.py
    ├── test_storage.py
    └── test_cli.py
```

## Commands

```sh
make test
make lint
make generate
make clean
make coverage
```

The `coverage` command generates a test coverage report using `coverage.py`.
HTML report is written to `htmlcov/index.html`.

## Dependencies

- Python >=3.11
- `antlr4-python3-runtime` (SQL parsing via ANTLR), dev: `antlr4-tools`, `mypy`, `pytest`
