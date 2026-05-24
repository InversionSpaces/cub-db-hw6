from dbms.errors import TypeMismatchError
from dbms.storage_protocol import SValue, StorageColumnDef, StorageColumnType, SIntValue, SBoolValue, STextValue


def validate_storage_value(val: SValue, col_def: StorageColumnDef, col_name: str) -> None:
    if col_def.type == StorageColumnType.INT:
        if not isinstance(val, SIntValue):
            raise TypeMismatchError(col_name, col_def.type.name, type(val).__name__)
    elif col_def.type == StorageColumnType.BOOL:
        if not isinstance(val, SBoolValue):
            raise TypeMismatchError(col_name, col_def.type.name, type(val).__name__)
    elif col_def.type == StorageColumnType.TEXT:
        if not isinstance(val, STextValue):
            raise TypeMismatchError(col_name, col_def.type.name, type(val).__name__)
    else:
        raise ValueError(f"Unknown column type: {col_def.type}")
