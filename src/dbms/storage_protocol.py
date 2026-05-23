from __future__ import annotations

from collections.abc import Sequence
from typing import Iterator, NewType, Protocol

PageId = NewType("PageId", int)
SlotId = NewType("SlotId", int)
RowId = tuple[PageId, SlotId]
TableName = NewType("TableName", str)
ItemOffset = NewType("ItemOffset", int)


class Storage(Protocol):
    def create_table(self, name: TableName, columns: Sequence[str]) -> None: ...
    def table_exists(self, name: TableName) -> bool: ...
    def get_columns(self, name: TableName) -> Sequence[str]: ...
    def get_tables(self) -> Sequence[TableName]: ...
    def insert_row(self, table: TableName, row: tuple[str, ...]) -> None:
        """Stage a row insertion. Not visible until commit."""
        ...
    def scan_rows(self, table: TableName) -> Iterator[tuple[RowId, tuple[str, ...]]]: ...
    def mark_update(self, table: TableName, row_id: RowId, new_row: tuple[str, ...]) -> None:
        """Stage a row update. Not visible until commit.
        
        RowId may be invalidated after commit. Re-scan to get fresh RowIds.
        Calling both mark_update and mark_delete on same RowId is undefined.
        """
        ...
    def mark_delete(self, table: TableName, row_id: RowId) -> None:
        """Stage a row deletion. Not visible until commit.
        
        Calling both mark_update and mark_delete on same RowId is undefined.
        """
        ...
    def commit(self) -> None: ...
    def vacuum(self) -> None: ...
    def close(self) -> None: ...
