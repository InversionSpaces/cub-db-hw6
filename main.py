import argparse
from pathlib import Path

from dbms.executor import Executor, SelectResult
from dbms.storage import FileStorage, TableName
from dbms.visitor import parse
from dbms.errors import DBMSError
from dbms.ast_nodes import BoolValue, IntValue, TextValue, Value


def format_value(v: Value) -> str:
    """Format a Value for display."""
    if isinstance(v, IntValue):
        return str(v.value)
    elif isinstance(v, BoolValue):
        return "TRUE" if v.value else "FALSE"
    elif isinstance(v, TextValue):
        return v.value
    return str(v)


def format_result(result: SelectResult | int | None | list[str]) -> str:
    match result:
        case None:
            return "OK"
        case int(count):
            return f"Affected rows: {count}"
        case SelectResult():
            if not result.rows:
                return "No rows"
            max_widths = [len(col) for col in result.columns]
            for row in result.rows:
                for i, val in enumerate(row):
                    max_widths[i] = max(max_widths[i], len(format_value(val)))
            lines = []
            header = " | ".join(col.ljust(max_widths[i]) for i, col in enumerate(result.columns))
            lines.append(header)
            separator = "-" * len(header)
            lines.append(separator)
            for row in result.rows:
                line = " | ".join(format_value(val).ljust(max_widths[i]) for i, val in enumerate(row))
                lines.append(line)
            return "\n".join(lines)
    return str(result)


def main() -> None:
    parser = argparse.ArgumentParser(description="DBMS CLI")
    parser.add_argument("file", type=Path, help="Database file path")
    args = parser.parse_args()

    store = FileStorage(args.file)
    executor = Executor(store)

    print(f"DBMS REPL. Database: {args.file}")
    print("Type 'exit' or 'quit' to exit.")
    print()

    while True:
        try:
            query = input("dbms> ")
        except EOFError:
            print()
            break

        query = query.strip()
        if not query:
            continue
        lower = query.lower()
        if lower in ("exit", "quit", "\\q"):
            break
        if lower == "help":
            print("Commands:")
            print("  help          - Show this help")
            print("  exit/quit/\\q  - Exit the REPL")
            print("  .tables       - List all tables")
            print("  VACUUM        - Optimize database file")
            print("  <SQL>         - Execute SQL statement")
            print()
            print("Supported SQL: CREATE TABLE, INSERT, SELECT, UPDATE, DELETE")
            continue
        if lower == ".tables" or lower == "tables":
            tables: list[TableName] = list(store.get_tables())
            if tables:
                print("Tables:")
                for t in sorted(tables, key=str):
                    cols = store.get_columns(t)
                    col_strs = [f"{c.name} {c.type.name}" for c in cols]
                    print(f"  {t} ({', '.join(col_strs)})")
            else:
                print("No tables")
            continue
        if lower == "vacuum":
            store.vacuum()
            print("OK")
            continue

        try:
            stmt = parse(query)
            result = executor.execute(stmt)
            store.commit()
            print(format_result(result))
        except DBMSError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"Error: {type(e).__name__}: {e}")

    store.close()


if __name__ == "__main__":
    main()
