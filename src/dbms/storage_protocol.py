from __future__ import annotations

import enum
from collections.abc import Sequence
from dataclasses import dataclass
from typing import Iterator, NewType, Protocol

PageId = NewType("PageId", int)
SlotId = NewType("SlotId", int)
RowId = tuple[PageId, SlotId]
TableName = NewType("TableName", str)
ItemOffset = NewType("ItemOffset", int)


class StorageColumnType(enum.Enum):
    INT = 0
    BOOL = 1
    TEXT = 2


@dataclass(frozen=True, slots=True)
class StorageColumnDef:
    name: str
    type: StorageColumnType


@dataclass(frozen=True, slots=True)
class SIntValue:
    value: int


@dataclass(frozen=True, slots=True)
class SBoolValue:
    value: bool


@dataclass(frozen=True, slots=True)
class STextValue:
    value: str


SValue = SIntValue | SBoolValue | STextValue
StorageRow = tuple[SValue, ...]


class Storage(Protocol):
    def create_table(self, name: TableName, columns: Sequence[StorageColumnDef]) -> None: ...
    def table_exists(self, name: TableName) -> bool: ...
    def get_columns(self, name: TableName) -> Sequence[StorageColumnDef]: ...
    def get_tables(self) -> Sequence[TableName]: ...
    def insert_row(self, table: TableName, row: StorageRow) -> None:
        """Stage a row insertion. Not visible until commit."""
        ...
    def scan_rows(self, table: TableName) -> Iterator[tuple[RowId, StorageRow]]: ...
    def mark_update(self, table: TableName, row_id: RowId, new_row: StorageRow) -> None:
        """Stage a row update. Not visible until commit.

        RowId may be invalidated after commit. Re-scan to get fresh RowIds.
        Calling both mark_update and mark_delete on same RowId is undefined.
        """
        ...
    def mark_delete(self, table: TableName, row_id: RowId) -> None:
        """Stage a row deletion. Not visible until commit.

        RowId may be invalidated after commit. Re-scan to get fresh RowIds.
        Calling both mark_update and mark_delete on same RowId is undefined.
        """
        ...
    def commit(self) -> None: ...
    def vacuum(self) -> None: ...
    def close(self) -> None: ...
