from __future__ import annotations

import enum
from dataclasses import dataclass
from typing import Literal, TypeAlias, Union


class ColumnType(enum.Enum):
    INT = "INT"
    BOOL = "BOOL"
    TEXT = "TEXT"


@dataclass(frozen=True)
class ColumnDef:
    name: str
    type: ColumnType


@dataclass(frozen=True)
class IntValue:
    value: int


@dataclass(frozen=True)
class BoolValue:
    value: bool


@dataclass(frozen=True)
class TextValue:
    value: str


Value: TypeAlias = IntValue | BoolValue | TextValue


Row = tuple[Value, ...]


@dataclass(frozen=True)
class WhereEq:
    column: str
    value: Value


@dataclass(frozen=True)
class WhereColEq:
    left: str
    right: str


@dataclass(frozen=True)
class WhereAnd:
    operands: tuple[WhereExpr, ...]


@dataclass(frozen=True)
class WhereOr:
    operands: tuple[WhereExpr, ...]


WhereExpr = WhereEq | WhereColEq | WhereAnd | WhereOr


@dataclass(frozen=True)
class Assignment:
    column: str
    value: Value


@dataclass(frozen=True)
class AssignmentColEq:
    left: str
    right: str


AssignmentExpr = Assignment | AssignmentColEq


@dataclass(frozen=True)
class CreateTableStmt:
    name: str
    columns: tuple[ColumnDef, ...]


@dataclass(frozen=True)
class InsertStmt:
    table: str
    columns: tuple[str, ...]
    values: tuple[Value, ...]


@dataclass(frozen=True)
class SelectStmt:
    table: str
    columns: tuple[str, ...] | Literal["*"]
    where: WhereExpr | None


@dataclass(frozen=True)
class UpdateStmt:
    table: str
    assignments: tuple[AssignmentExpr, ...]
    where: WhereExpr | None


@dataclass(frozen=True)
class DeleteStmt:
    table: str
    where: WhereExpr | None


Statement = CreateTableStmt | InsertStmt | SelectStmt | UpdateStmt | DeleteStmt


@dataclass
class TableDef:
    name: str
    columns: tuple[ColumnDef, ...]


def value_type(v: Value) -> ColumnType:
    """Return the ColumnType of a Value instance."""
    if isinstance(v, IntValue):
        return ColumnType.INT
    if isinstance(v, BoolValue):
        return ColumnType.BOOL
    if isinstance(v, TextValue):
        return ColumnType.TEXT
    raise TypeError(f"Unknown value type: {type(v)}")


