from __future__ import annotations


class DBMSError(Exception):
    pass


class ParseError(DBMSError):
    pass


class TableNotFoundError(DBMSError):
    pass


class ColumnMismatchError(DBMSError):
    pass


class RowTooLargeError(DBMSError):
    pass


class DuplicateTableError(DBMSError):
    pass


class DuplicateColumnError(DBMSError):
    pass


class RowNotFoundError(DBMSError):
    pass


class CorruptFileError(DBMSError):
    pass


class TypeMismatchError(DBMSError):
    def __init__(self, column: str, expected: str, got: str) -> None:
        self.column = column
        self.expected = expected
        self.got = got
        super().__init__(f"Column '{column}' expected {expected}, got {got}")


class IntegerOverflowError(DBMSError):
    pass