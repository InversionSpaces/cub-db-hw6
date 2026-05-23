# Simple File-Based DBMS

A Python file-based DBMS supporting multiple named tables with string-only columns. Uses a PostgreSQL-style slotted page binary storage format and ANTLR for SQL parsing. Java is required to regenerate the parser.

## Project Structure

```
hw6/
├── pyproject.toml
├── Makefile
├── grammar/
│   └── SimpleSQL.g4
├── src/dbms/
│   ├── __init__.py
│   ├── ast_nodes.py
│   ├── errors.py
│   ├── visitor.py
│   ├── generated/
│   │   ├── SimpleSQLLexer.py
│   │   ├── SimpleSQLParser.py
│   │   └── SimpleSQLVisitor.py
│   ├── storage.py
│   ├── executor.py
│   └── cli.py
└── tests/
    ├── conftest.py
    ├── test_ast.py
    └── test_visitor.py
```

## Dependencies

- Python >=3.11
- Java (for ANTLR parser generation)
- `antlr4-python3-runtime`, dev: `mypy`, `pytest`

## Commands

```sh
make test
make lint
make generate
make clean
```

## SQL Syntax

```sql
CREATE TABLE <name> (<col>, ...)
INSERT INTO <name> (<col>, ...) VALUES (<val>, ...)
SELECT <col>, ... | * FROM <name> [WHERE <expr>]
UPDATE <name> SET <col> = <val>, ... [WHERE <expr>]
DELETE FROM <name> [WHERE <expr>]
```

WHERE expressions support `AND` (higher precedence), `OR`, and parenthesized grouping:

```sql
WHERE a = '1' AND b = '2' OR c = '3'   -- (a AND b) OR c
WHERE (a = '1' OR b = '2') AND c = '3' -- grouped OR with AND
```

All values are string literals using single quotes. Double single quotes to escape: `'it''s'`.