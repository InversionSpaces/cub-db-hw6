from __future__ import annotations

from collections.abc import Sequence
from typing import Iterator, NewType, Protocol

PageId = NewType("PageId", int)
SlotId = NewType("SlotId", int)
RowId = tuple[PageId, SlotId]


class Storage(Protocol):
    def create_table(self, name: str, columns: Sequence[str]) -> None: ...
    def table_exists(self, name: str) -> bool: ...
    def get_columns(self, name: str) -> Sequence[str]: ...
    def insert_row(self, table: str, row: tuple[str, ...]) -> None:
        """Stage a row insertion. Not visible until commit."""
        ...
    def scan_rows(self, table: str) -> Iterator[tuple[RowId, tuple[str, ...]]]: ...
    def mark_update(self, table: str, row_id: RowId, new_row: tuple[str, ...]) -> None:
        """Stage a row update. Not visible until commit.
        
        RowId may be invalidated after commit. Re-scan to get fresh RowIds.
        Calling both mark_update and mark_delete on same RowId is undefined.
        """
        ...
    def mark_delete(self, table: str, row_id: RowId) -> None:
        """Stage a row deletion. Not visible until commit.
        
        Calling both mark_update and mark_delete on same RowId is undefined.
        """
        ...
    def commit(self) -> None: ...
    def vacuum(self) -> None: ...
    def close(self) -> None: ...
