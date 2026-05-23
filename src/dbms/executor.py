from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass

from dbms.ast_nodes import (
    Assignment,
    AssignmentColEq,
    AssignmentExpr,
    CreateTableStmt,
    DeleteStmt,
    InsertStmt,
    Row,
    SelectStmt,
    Statement,
    UpdateStmt,
    WhereAnd,
    WhereColEq,
    WhereEq,
    WhereExpr,
    WhereOr,
)
from dbms.storage_protocol import RowId
from dbms.errors import (
    ColumnMismatchError,
    DuplicateColumnError,
    DuplicateTableError,
    TableNotFoundError,
)
from dbms.storage_protocol import Storage


@dataclass
class SelectResult:
    rows: tuple[Row, ...]
    columns: tuple[str, ...]


class Executor:
    def __init__(self, store: Storage) -> None:
        self._store = store

    def execute(self, stmt: Statement) -> SelectResult | int | None:
        match stmt:
            case CreateTableStmt():
                self.create_table(stmt)
                return None
            case InsertStmt():
                return self.insert(stmt)
            case SelectStmt():
                return self.select(stmt)
            case UpdateStmt():
                return self.update(stmt)
            case DeleteStmt():
                return self.delete(stmt)

    def create_table(self, stmt: CreateTableStmt) -> None:
        seen: set[str] = set()
        for col in stmt.columns:
            if col in seen:
                raise DuplicateColumnError(col)
            seen.add(col)
        if self._store.table_exists(stmt.name):
            raise DuplicateTableError(stmt.name)
        self._store.create_table(stmt.name, stmt.columns)

    def insert(self, stmt: InsertStmt) -> int:
        if not self._store.table_exists(stmt.table):
            raise TableNotFoundError(stmt.table)
        columns = self._store.get_columns(stmt.table)
        if len(stmt.columns) != len(stmt.values):
            raise ColumnMismatchError(
                f"{len(stmt.columns)} columns but {len(stmt.values)} values"
            )
        if set(stmt.columns) != set(columns):
            raise ColumnMismatchError(
                f"Insert columns {stmt.columns} do not match table columns {columns}"
            )
        col_index = {name: i for i, name in enumerate(stmt.columns)}
        row = tuple(
            stmt.values[col_index[columns[i]]]
            for i in range(len(columns))
        )
        self._store.insert_row(stmt.table, row)
        return 1

    def _validate_where_columns(self, where: WhereExpr | None, columns: Sequence[str]) -> None:
        match where:
            case None:
                pass
            case WhereEq(column=col, value=_):
                if col not in columns:
                    raise ColumnMismatchError(col)
            case WhereColEq(left=l, right=r):
                if l not in columns:
                    raise ColumnMismatchError(l)
                if r not in columns:
                    raise ColumnMismatchError(r)
            case WhereAnd(operands=ops) | WhereOr(operands=ops):
                for op in ops:
                    self._validate_where_columns(op, columns)

    def select(self, stmt: SelectStmt) -> SelectResult:
        if not self._store.table_exists(stmt.table):
            raise TableNotFoundError(stmt.table)
        columns = self._store.get_columns(stmt.table)
        self._validate_where_columns(stmt.where, columns)
        if stmt.columns == "*":
            out_cols: Sequence[str] = columns
        else:
            if any(col not in columns for col in stmt.columns):
                raise ColumnMismatchError(
                    next(col for col in stmt.columns if col not in columns)
                )
            out_cols = stmt.columns
        col_index = {c: i for i, c in enumerate(columns)}
        result_rows: list[Row] = []
        for _, row in self._store.scan_rows(stmt.table):
            if self._evaluate_where(stmt.where, row, columns, col_index):
                result_rows.append(self._project(row, out_cols, col_index))
        return SelectResult(rows=tuple(result_rows), columns=tuple(out_cols))

    def update(self, stmt: UpdateStmt) -> int:
        if not self._store.table_exists(stmt.table):
            raise TableNotFoundError(stmt.table)
        columns = self._store.get_columns(stmt.table)
        self._validate_where_columns(stmt.where, columns)
        for assign in stmt.assignments:
            col = assign.column if isinstance(assign, Assignment) else assign.left
            if col not in columns:
                raise ColumnMismatchError(col)
            if isinstance(assign, AssignmentColEq) and assign.right not in columns:
                raise ColumnMismatchError(assign.right)
        col_index = {c: i for i, c in enumerate(columns)}
        count = 0
        for row_id, row in self._store.scan_rows(stmt.table):
            if not self._evaluate_where(stmt.where, row, columns, col_index):
                continue
            new_row = self._apply_assignments(stmt.assignments, row, columns)
            self._store.mark_update(stmt.table, row_id, new_row)
            count += 1
        if count > 0:
            self._store.commit()
        return count

    def delete(self, stmt: DeleteStmt) -> int:
        if not self._store.table_exists(stmt.table):
            raise TableNotFoundError(stmt.table)
        columns = self._store.get_columns(stmt.table)
        self._validate_where_columns(stmt.where, columns)
        col_index = {c: i for i, c in enumerate(columns)}
        count = 0
        for row_id, row in self._store.scan_rows(stmt.table):
            if self._evaluate_where(stmt.where, row, columns, col_index):
                self._store.mark_delete(stmt.table, row_id)
                count += 1
        if count > 0:
            self._store.commit()
        return count

    def _evaluate_where(
        self,
        where: WhereExpr | None,
        row: Row,
        columns: Sequence[str],
        col_index: dict[str, int],
    ) -> bool:
        match where:
            case None:
                return True
            case WhereEq(column=col, value=val):
                if col not in columns:
                    raise ColumnMismatchError(col)
                return row[col_index[col]] == val
            case WhereColEq(left=l, right=r):
                if l not in columns:
                    raise ColumnMismatchError(l)
                if r not in columns:
                    raise ColumnMismatchError(r)
                return row[col_index[l]] == row[col_index[r]]
            case WhereAnd(operands=ops):
                return all(self._evaluate_where(op, row, columns, col_index) for op in ops)
            case WhereOr(operands=ops):
                return any(self._evaluate_where(op, row, columns, col_index) for op in ops)

    def _project(self, row: Row, out_cols: Sequence[str], col_index: dict[str, int]) -> Row:
        return tuple(row[col_index[c]] for c in out_cols)

    def _apply_assignments(
        self, assignments: tuple[AssignmentExpr, ...], row: Row, columns: Sequence[str]
    ) -> Row:
        row_dict = dict(zip(columns, row))
        old_values = dict(row_dict)
        for assign in assignments:
            match assign:
                case Assignment(column=col, value=val):
                    row_dict[col] = val
                case AssignmentColEq(left=col1, right=col2):
                    row_dict[col1] = old_values[col2]
        return tuple(row_dict[c] for c in columns)