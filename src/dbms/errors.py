from __future__ import annotations


class DBMSError(Exception):
    pass


class ParseError(DBMSError):
    pass


class TableNotFoundError(DBMSError):
    pass


class ColumnMismatchError(DBMSError):
    pass


class DuplicateTableError(DBMSError):
    pass