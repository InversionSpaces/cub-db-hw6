from __future__ import annotations

from collections.abc import Sequence
from typing import Iterator, TYPE_CHECKING

from dbms.errors import ColumnMismatchError, DuplicateTableError, TableNotFoundError
from dbms.storage_protocol import PageId, RowId, SlotId, Storage

if TYPE_CHECKING:
    Row = tuple[str, ...]


class InMemoryStorage:
    def __init__(self) -> None:
        self._tables: dict[str, tuple[str, ...]] = {}
        self._rows: dict[str, dict[RowId, tuple[str, ...]]] = {}
        self._next_id: dict[str, int] = {}
        self._pending_updates: dict[str, dict[RowId, tuple[str, ...]]] = {}
        self._pending_deletes: dict[str, set[RowId]] = {}

    def create_table(self, name: str, columns: Sequence[str]) -> None:
        if name in self._tables:
            raise DuplicateTableError(name)
        self._tables[name] = tuple(columns)
        self._rows[name] = {}
        self._next_id[name] = 0

    def table_exists(self, name: str) -> bool:
        return name in self._tables

    def get_columns(self, name: str) -> Sequence[str]:
        self._require_table(name)
        return self._tables[name]

    def insert_row(self, table: str, row: tuple[str, ...]) -> None:
        self._require_table(table)
        columns = self._tables[table]
        if len(row) != len(columns):
            raise ColumnMismatchError(
                f"Expected {len(columns)} values, got {len(row)}"
            )
        rid: RowId = (PageId(0), SlotId(self._next_id[table]))
        self._rows[table][rid] = row
        self._next_id[table] = self._next_id[table] + 1

    def scan_rows(self, table: str) -> Iterator[tuple[RowId, tuple[str, ...]]]:
        self._require_table(table)
        yield from self._rows[table].items()

    def mark_update(self, table: str, row_id: RowId, new_row: tuple[str, ...]) -> None:
        self._require_table(table)
        columns = self._tables[table]
        if len(new_row) != len(columns):
            raise ColumnMismatchError(
                f"Expected {len(columns)} values, got {len(new_row)}"
            )
        if table not in self._pending_updates:
            self._pending_updates[table] = {}
        self._pending_updates[table][row_id] = new_row

    def mark_delete(self, table: str, row_id: RowId) -> None:
        self._require_table(table)
        if table not in self._pending_deletes:
            self._pending_deletes[table] = set()
        self._pending_deletes[table].add(row_id)

    def commit(self) -> None:
        for table, updates in self._pending_updates.items():
            for row_id, new_row in updates.items():
                if table in self._pending_deletes and row_id in self._pending_deletes[table]:
                    continue
                if row_id in self._rows[table]:
                    self._rows[table][row_id] = new_row
        for table, row_ids in self._pending_deletes.items():
            for row_id in row_ids:
                self._rows[table].pop(row_id, None)
        self._pending_updates.clear()
        self._pending_deletes.clear()

    def vacuum(self) -> None:
        self.commit()

    def close(self) -> None:
        pass

    def _require_table(self, name: str) -> None:
        if name not in self._tables:
            raise TableNotFoundError(name)
