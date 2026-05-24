from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass

from dbms.ast_nodes import (
    Assignment,
    AssignmentColEq,
    AssignmentExpr,
    BoolValue,
    ColumnDef,
    ColumnType,
    CreateTableStmt,
    DeleteStmt,
    IntValue,
    InsertStmt,
    Row,
    SelectStmt,
    Statement,
    TextValue,
    UpdateStmt,
    Value,
    WhereAnd,
    WhereColEq,
    WhereEq,
    WhereExpr,
    WhereOr,
    value_type,
)
from dbms.storage_protocol import (
    SBoolValue,
    SIntValue,
    Storage,
    StorageColumnDef,
    StorageColumnType,
    StorageRow,
    STextValue,
    TableName,
)
from dbms.errors import (
    ColumnMismatchError,
    DuplicateColumnError,
    DuplicateTableError,
    TableNotFoundError,
    TypeMismatchError,
)


@dataclass
class SelectResult:
    rows: tuple[Row, ...]
    columns: tuple[str, ...]


def _coldef_to_storage(cd: ColumnDef) -> StorageColumnDef:
    if cd.type == ColumnType.INT:
        st = StorageColumnType.INT
    elif cd.type == ColumnType.BOOL:
        st = StorageColumnType.BOOL
    elif cd.type == ColumnType.TEXT:
        st = StorageColumnType.TEXT
    else:
        raise ValueError(f"Unknown column type: {cd.type}")
    return StorageColumnDef(name=cd.name, type=st)


def _coldef_from_storage(cd: StorageColumnDef) -> ColumnDef:
    if cd.type == StorageColumnType.INT:
        at = ColumnType.INT
    elif cd.type == StorageColumnType.BOOL:
        at = ColumnType.BOOL
    elif cd.type == StorageColumnType.TEXT:
        at = ColumnType.TEXT
    else:
        raise ValueError(f"Unknown storage column type: {cd.type}")
    return ColumnDef(name=cd.name, type=at)


def _value_to_storage(v: Value) -> SIntValue | SBoolValue | STextValue:
    if isinstance(v, IntValue):
        return SIntValue(value=v.value)
    elif isinstance(v, BoolValue):
        return SBoolValue(value=v.value)
    elif isinstance(v, TextValue):
        return STextValue(value=v.value)
    raise ValueError(f"Unknown value type: {type(v)}")


def _value_from_storage(v: SIntValue | SBoolValue | STextValue) -> Value:
    if isinstance(v, SIntValue):
        return IntValue(value=v.value)
    elif isinstance(v, SBoolValue):
        return BoolValue(value=v.value)
    elif isinstance(v, STextValue):
        return TextValue(value=v.value)
    raise ValueError(f"Unknown storage value type: {type(v)}")


def _row_to_storage(row: Row) -> StorageRow:
    return tuple(_value_to_storage(v) for v in row)


def _row_from_storage(row: StorageRow) -> Row:
    return tuple(_value_from_storage(v) for v in row)


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
            if col.name in seen:
                raise DuplicateColumnError(col.name)
            seen.add(col.name)
        table_name = TableName(stmt.name)
        if self._store.table_exists(table_name):
            raise DuplicateTableError(stmt.name)
        storage_cols = tuple(_coldef_to_storage(cd) for cd in stmt.columns)
        self._store.create_table(table_name, storage_cols)

    def insert(self, stmt: InsertStmt) -> int:
        table_name = TableName(stmt.table)
        if not self._store.table_exists(table_name):
            raise TableNotFoundError(stmt.table)
        columns = self._get_table_columns(table_name)
        
        if not stmt.value_rows:
            raise ColumnMismatchError("No values provided")
        for row_idx, value_row in enumerate(stmt.value_rows):
            if len(stmt.columns) != len(value_row):
                raise ColumnMismatchError(
                    f"{len(stmt.columns)} columns but {len(value_row)} values in row {row_idx + 1}"
                )
        if set(stmt.columns) != set(c.name for c in columns):
            raise ColumnMismatchError(
                f"Insert columns {stmt.columns} do not match table columns {[c.name for c in columns]}"
            )
        col_index = {name: i for i, name in enumerate(stmt.columns)}
        count = 0
        for value_row in stmt.value_rows:
            final_row: tuple[Value, ...] = tuple(
                value_row[col_index[c.name]] for c in columns
            )
            for val, col in zip(final_row, columns):
                actual_type = value_type(val)
                if actual_type != col.type:
                    raise TypeMismatchError(col.name, col.type.value, actual_type.value)
            
            storage_row = _row_to_storage(final_row)
            self._store.insert_row(table_name, storage_row)
            count += 1
        
        if count > 0:
            self._store.commit()
        return count

    def _get_table_columns(self, table_name: TableName) -> Sequence[ColumnDef]:
        storage_cols = self._store.get_columns(table_name)
        return tuple(_coldef_from_storage(cd) for cd in storage_cols)

    def _validate_where_columns_and_types(
        self, where: WhereExpr | None, columns: Sequence[ColumnDef]
    ) -> None:
        col_map = {c.name: c for c in columns}
        match where:
            case None:
                pass
            case WhereEq(column=col, value=val):
                if col not in col_map:
                    raise ColumnMismatchError(col)
                expected_type = col_map[col].type
                actual_type = value_type(val)
                if actual_type != expected_type:
                    raise TypeMismatchError(col, expected_type.value, actual_type.value)
            case WhereColEq(left=l, right=r):
                if l not in col_map:
                    raise ColumnMismatchError(l)
                if r not in col_map:
                    raise ColumnMismatchError(r)
                left_type = col_map[l].type
                right_type = col_map[r].type
                if left_type != right_type:
                    raise TypeMismatchError(l, left_type.value, right_type.value)
            case WhereAnd(operands=ops) | WhereOr(operands=ops):
                for op in ops:
                    self._validate_where_columns_and_types(op, columns)

    def _evaluate_where(
        self,
        where: WhereExpr | None,
        row: Row,
        columns: Sequence[ColumnDef],
        col_index: dict[str, int],
    ) -> bool:
        match where:
            case None:
                return True
            case WhereEq(column=col, value=val):
                idx = col_index[col]
                return row[idx].value == val.value
            case WhereColEq(left=l, right=r):
                li = col_index[l]
                ri = col_index[r]
                return row[li].value == row[ri].value
            case WhereAnd(operands=ops):
                return all(self._evaluate_where(op, row, columns, col_index) for op in ops)
            case WhereOr(operands=ops):
                return any(self._evaluate_where(op, row, columns, col_index) for op in ops)
        return False

    def select(self, stmt: SelectStmt) -> SelectResult:
        table_name = TableName(stmt.table)
        if not self._store.table_exists(table_name):
            raise TableNotFoundError(stmt.table)
        columns = self._get_table_columns(table_name)
        self._validate_where_columns_and_types(stmt.where, columns)
        col_index = {c.name: i for i, c in enumerate(columns)}
        if stmt.columns == "*":
            out_cols: Sequence[str] = tuple(c.name for c in columns)
        else:
            for col in stmt.columns:
                if col not in col_index:
                    raise ColumnMismatchError(col)
            out_cols = stmt.columns
        result_rows: list[Row] = []
        for _, storage_row in self._store.scan_rows(table_name):
            row = _row_from_storage(storage_row)
            if self._evaluate_where(stmt.where, row, columns, col_index):
                result_rows.append(self._project(row, out_cols, col_index))
        return SelectResult(rows=tuple(result_rows), columns=tuple(out_cols))

    def _validate_assignment_types(
        self, assign: AssignmentExpr, columns: Sequence[ColumnDef]
    ) -> None:
        col_map = {c.name: c for c in columns}
        if isinstance(assign, Assignment):
            col = assign.column
            if col not in col_map:
                raise ColumnMismatchError(col)
            expected_type = col_map[col].type
            actual_type = value_type(assign.value)
            if actual_type != expected_type:
                raise TypeMismatchError(col, expected_type.value, actual_type.value)
        elif isinstance(assign, AssignmentColEq):
            left = assign.left
            right = assign.right
            if left not in col_map:
                raise ColumnMismatchError(left)
            if right not in col_map:
                raise ColumnMismatchError(right)
            left_type = col_map[left].type
            right_type = col_map[right].type
            if left_type != right_type:
                raise TypeMismatchError(left, left_type.value, right_type.value)

    def update(self, stmt: UpdateStmt) -> int:
        table_name = TableName(stmt.table)
        if not self._store.table_exists(table_name):
            raise TableNotFoundError(stmt.table)
        columns = self._get_table_columns(table_name)
        self._validate_where_columns_and_types(stmt.where, columns)
        for assign in stmt.assignments:
            self._validate_assignment_types(assign, columns)
        col_index = {c.name: i for i, c in enumerate(columns)}
        count = 0
        for row_id, storage_row in self._store.scan_rows(table_name):
            row = _row_from_storage(storage_row)
            if not self._evaluate_where(stmt.where, row, columns, col_index):
                continue
            new_row = self._apply_assignments(stmt.assignments, row, columns, col_index)
            storage_new_row = _row_to_storage(new_row)
            self._store.mark_update(table_name, row_id, storage_new_row)
            count += 1
        if count > 0:
            self._store.commit()
        return count

    def delete(self, stmt: DeleteStmt) -> int:
        table_name = TableName(stmt.table)
        if not self._store.table_exists(table_name):
            raise TableNotFoundError(stmt.table)
        columns = self._get_table_columns(table_name)
        self._validate_where_columns_and_types(stmt.where, columns)
        col_index = {c.name: i for i, c in enumerate(columns)}
        count = 0
        for row_id, storage_row in self._store.scan_rows(table_name):
            row = _row_from_storage(storage_row)
            if self._evaluate_where(stmt.where, row, columns, col_index):
                self._store.mark_delete(table_name, row_id)
                count += 1
        if count > 0:
            self._store.commit()
        return count

    def _project(
        self, row: Row, out_cols: Sequence[str], col_index: dict[str, int]
    ) -> Row:
        return tuple(row[col_index[c]] for c in out_cols)

    def _apply_assignments(
        self,
        assignments: tuple[AssignmentExpr, ...],
        row: Row,
        columns: Sequence[ColumnDef],
        col_index: dict[str, int],
    ) -> Row:
        row_dict = dict(zip((c.name for c in columns), row))
        old_values = dict(row_dict)
        for assign in assignments:
            match assign:
                case Assignment(column=col, value=val):
                    row_dict[col] = val
                case AssignmentColEq(left=col1, right=col2):
                    row_dict[col1] = old_values[col2]
        return tuple(row_dict[c.name] for c in columns)
