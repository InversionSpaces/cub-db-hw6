from __future__ import annotations

from dataclasses import dataclass
from typing import Literal


Row = tuple[str, ...]


@dataclass(frozen=True)
class WhereEq:
    column: str
    value: str


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
    value: str


@dataclass(frozen=True)
class AssignmentColEq:
    left: str
    right: str


AssignmentExpr = Assignment | AssignmentColEq


@dataclass(frozen=True)
class CreateTableStmt:
    name: str
    columns: tuple[str, ...]


@dataclass(frozen=True)
class InsertStmt:
    table: str
    columns: tuple[str, ...]
    values: tuple[str, ...]


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
    columns: tuple[str, ...]


