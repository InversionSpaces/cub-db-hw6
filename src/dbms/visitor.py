from __future__ import annotations

from typing import Literal

from antlr4 import CommonTokenStream, InputStream
from antlr4.error.ErrorListener import ErrorListener

from dbms.ast_nodes import (
    Assignment,
    AssignmentColEq,
    AssignmentExpr,
    BoolValue,
    ColumnDef,
    ColumnType,
    CreateTableStmt,
    DeleteStmt,
    InsertStmt,
    IntValue,
    SelectStmt,
    Statement,
    TableDef,
    TextValue,
    UpdateStmt,
    Value,
    WhereAnd,
    WhereColEq,
    WhereEq,
    WhereExpr,
    WhereOr,
)
from dbms.errors import IntegerOverflowError, ParseError
from dbms.generated.SimpleSQLLexer import SimpleSQLLexer
from dbms.generated.SimpleSQLParser import SimpleSQLParser
from dbms.generated.SimpleSQLVisitor import SimpleSQLVisitor


class _ErrorListener(ErrorListener):
    def syntaxError(
        self,
        recognizer: object,
        offendingSymbol: object,
        line: int,
        column: int,
        msg: str,
        e: object,
    ) -> None:
        raise ParseError(f"Syntax error at line {line}:{column}: {msg}")


def parse(sql: str) -> Statement:
    input_stream = InputStream(sql)
    lexer = SimpleSQLLexer(input_stream)
    lexer.removeErrorListeners()
    lexer.addErrorListener(_ErrorListener())

    token_stream = CommonTokenStream(lexer)
    parser = SimpleSQLParser(token_stream)
    parser.removeErrorListeners()
    parser.addErrorListener(_ErrorListener())

    tree = parser.statement()
    visitor = _ASTVisitor()
    result: Statement = visitor.visit(tree)
    if result is None:
        raise ParseError("Failed to parse statement")
    return result


def _strip_quotes(s: str) -> str:
    if s.startswith("'") and s.endswith("'"):
        inner = s[1:-1]
        return inner.replace("''", "'")
    return s


class _ASTVisitor(SimpleSQLVisitor):
    def visitStatement(self, ctx: SimpleSQLParser.StatementContext) -> Statement:
        if ctx.createTable():
            return self.visitCreateTable(ctx.createTable())
        if ctx.insertInto():
            return self.visitInsertInto(ctx.insertInto())
        if ctx.selectStmt():
            return self.visitSelectStmt(ctx.selectStmt())
        if ctx.updateStmt():
            return self.visitUpdateStmt(ctx.updateStmt())
        if ctx.deleteStmt():
            return self.visitDeleteStmt(ctx.deleteStmt())
        raise ParseError("Unknown statement type")

    def visitCreateTable(self, ctx: SimpleSQLParser.CreateTableContext) -> CreateTableStmt:
        name = ctx.identifier().IDENTIFIER().getText()
        columns = self.visitColumnDefList(ctx.columnDefList())
        return CreateTableStmt(name=name, columns=columns)

    def visitColumnDefList(self, ctx: SimpleSQLParser.ColumnDefListContext) -> tuple[ColumnDef, ...]:
        column_defs = ctx.columnDef()
        return tuple(self.visitColumnDef(cd) for cd in column_defs)

    def visitColumnDef(self, ctx: SimpleSQLParser.ColumnDefContext) -> ColumnDef:
        name = ctx.identifier().IDENTIFIER().getText()
        col_type = self.visitTypeName(ctx.typeName())
        return ColumnDef(name=name, type=col_type)

    def visitTypeName(self, ctx: SimpleSQLParser.TypeNameContext) -> ColumnType:
        if ctx.INT_T():
            return ColumnType.INT
        if ctx.BOOL_T():
            return ColumnType.BOOL
        if ctx.TEXT_T():
            return ColumnType.TEXT
        raise ParseError(f"Unknown type name at {ctx.start.line}:{ctx.start.column}")

    def visitInsertInto(self, ctx: SimpleSQLParser.InsertIntoContext) -> InsertStmt:
        table = ctx.identifier().IDENTIFIER().getText()
        columns = self.visitColumnList(ctx.columnList())
        values = self.visitValueList(ctx.valueList())
        return InsertStmt(table=table, columns=columns, values=values)

    def visitSelectStmt(self, ctx: SimpleSQLParser.SelectStmtContext) -> SelectStmt:
        table = ctx.identifier().IDENTIFIER().getText()
        cols = self.visitSelectColumns(ctx.selectColumns())
        where: WhereExpr | None = None
        if ctx.whereExpr():
            where = self.visitWhereExpr(ctx.whereExpr())
        return SelectStmt(table=table, columns=cols, where=where)

    def visitUpdateStmt(self, ctx: SimpleSQLParser.UpdateStmtContext) -> UpdateStmt:
        table = ctx.identifier().IDENTIFIER().getText()
        assignments = self.visitAssignmentList(ctx.assignmentList())
        where: WhereExpr | None = None
        if ctx.whereExpr():
            where = self.visitWhereExpr(ctx.whereExpr())
        return UpdateStmt(table=table, assignments=assignments, where=where)

    def visitDeleteStmt(self, ctx: SimpleSQLParser.DeleteStmtContext) -> DeleteStmt:
        table = ctx.identifier().IDENTIFIER().getText()
        where: WhereExpr | None = None
        if ctx.whereExpr():
            where = self.visitWhereExpr(ctx.whereExpr())
        return DeleteStmt(table=table, where=where)

    def visitSelectColumns(
        self, ctx: SimpleSQLParser.SelectColumnsContext
    ) -> tuple[str, ...] | Literal["*"]:
        if ctx.STAR():
            return "*"
        return self.visitColumnList(ctx.columnList())

    def visitColumnList(self, ctx: SimpleSQLParser.ColumnListContext) -> tuple[str, ...]:
        identifiers = ctx.identifier()
        return tuple(ident.IDENTIFIER().getText() for ident in identifiers)

    def visitValueList(self, ctx: SimpleSQLParser.ValueListContext) -> tuple[Value, ...]:
        value_lits = ctx.valueLit()
        return tuple(self.visitValueLit(vl) for vl in value_lits)

    def visitValueLit(self, ctx: SimpleSQLParser.ValueLitContext) -> Value:
        if ctx.INTEGER_LITERAL():
            text = ctx.INTEGER_LITERAL().getText()
            try:
                val = int(text)
            except ValueError:
                raise ParseError(f"Invalid integer literal: {text}")
            if val < -2**31 or val > 2**31 - 1:
                raise IntegerOverflowError(
                    f"Integer {val} out of range for INT ({-2**31}..{2**31 - 1})"
                )
            return IntValue(value=val)
        if ctx.TRUE():
            return BoolValue(value=True)
        if ctx.FALSE():
            return BoolValue(value=False)
        if ctx.stringLiteral():
            raw = ctx.stringLiteral().STRING_LITERAL().getText()
            return TextValue(value=_strip_quotes(raw))
        raise ParseError(f"Unknown value literal at {ctx.start.line}:{ctx.start.column}")

    def visitWhereExpr(self, ctx: SimpleSQLParser.WhereExprContext) -> WhereExpr:
        return self.visitWhereOr(ctx.whereOr())

    def visitWhereOr(self, ctx: SimpleSQLParser.WhereOrContext) -> WhereExpr:
        ands = ctx.whereAnd()
        if len(ands) == 1:
            return self.visitWhereAnd(ands[0])
        return WhereOr(
            operands=tuple(self.visitWhereAnd(a) for a in ands)
        )

    def visitWhereAnd(self, ctx: SimpleSQLParser.WhereAndContext) -> WhereExpr:
        atoms = ctx.whereAtom()
        if len(atoms) == 1:
            return self.visitWhereAtom(atoms[0])
        return WhereAnd(
            operands=tuple(self.visitWhereAtom(a) for a in atoms)
        )

    def visitWhereAtom(self, ctx: SimpleSQLParser.WhereAtomContext) -> WhereExpr:
        if ctx.LPAREN():
            return self.visitWhereExpr(ctx.whereExpr())
        identifiers = ctx.identifier()
        if ctx.valueLit():
            col = identifiers[0].IDENTIFIER().getText()
            val = self.visitValueLit(ctx.valueLit())
            return WhereEq(column=col, value=val)
        left = identifiers[0].IDENTIFIER().getText()
        right = identifiers[1].IDENTIFIER().getText()
        return WhereColEq(left=left, right=right)

    def visitAssignmentList(
        self, ctx: SimpleSQLParser.AssignmentListContext
    ) -> tuple[AssignmentExpr, ...]:
        assignments = ctx.assignment()
        return tuple(self.visitAssignment(a) for a in assignments)

    def visitAssignment(self, ctx: SimpleSQLParser.AssignmentContext) -> AssignmentExpr:
        identifiers = ctx.identifier()
        col = identifiers[0].IDENTIFIER().getText()
        if ctx.valueLit():
            val = self.visitValueLit(ctx.valueLit())
            return Assignment(column=col, value=val)
        right = identifiers[1].IDENTIFIER().getText()
        return AssignmentColEq(left=col, right=right)

    def visitIdentifier(self, ctx: SimpleSQLParser.IdentifierContext) -> str:
        return str(ctx.IDENTIFIER().getText())

    def visitStringLiteral(self, ctx: SimpleSQLParser.StringLiteralContext) -> str:
        return _strip_quotes(str(ctx.STRING_LITERAL().getText()))
