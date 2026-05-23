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

## Dependencies

- Python >=3.11
- `antlr4-python3-runtime` (SQL parsing via ANTLR), dev: `antlr4-tools`, `mypy`, `pytest`

## Commands

```sh
make test
make lint
make generate
make clean
```

## Architecture

Uses a PostgreSQL-style slotted page binary storage format.

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
    └── test_storage.py
```

## Known Limitations

### Metadata Durability
Metadata chain extensions are not atomic. A crash during commit may leave the metadata chain in an inconsistent state.

### Bulk Insert Performance
Large bulk inserts degrade to O(N^2) time due to linear page-chain scanning for free space.

### Memory Pressure in Long Transactions
Modified pages cannot be evicted until commit. Long transactions that modify many pages will grow the cache unbounded. Commit frequently to avoid memory pressure.
