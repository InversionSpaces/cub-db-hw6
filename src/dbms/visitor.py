from __future__ import annotations

from typing import Literal

from antlr4 import CommonTokenStream, InputStream
from antlr4.error.ErrorListener import ErrorListener

from dbms.ast_nodes import (
    Assignment,
    AssignmentColEq,
    AssignmentExpr,
    CreateTableStmt,
    DeleteStmt,
    InsertStmt,
    SelectStmt,
    Statement,
    UpdateStmt,
    WhereAnd,
    WhereColEq,
    WhereEq,
    WhereExpr,
    WhereOr,
)
from dbms.errors import ParseError
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
        columns = self.visitColumnList(ctx.columnList())
        return CreateTableStmt(name=name, columns=columns)

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

    def visitValueList(self, ctx: SimpleSQLParser.ValueListContext) -> tuple[str, ...]:
        literals = ctx.stringLiteral()
        return tuple(_strip_quotes(lit.STRING_LITERAL().getText()) for lit in literals)

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
        if ctx.stringLiteral():
            col = identifiers[0].IDENTIFIER().getText()
            val = _strip_quotes(ctx.stringLiteral().STRING_LITERAL().getText())
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
        if ctx.stringLiteral():
            val = _strip_quotes(ctx.stringLiteral().STRING_LITERAL().getText())
            return Assignment(column=col, value=val)
        right = identifiers[1].IDENTIFIER().getText()
        return AssignmentColEq(left=col, right=right)

    def visitIdentifier(self, ctx: SimpleSQLParser.IdentifierContext) -> str:
        return str(ctx.IDENTIFIER().getText())

    def visitStringLiteral(self, ctx: SimpleSQLParser.StringLiteralContext) -> str:
        return _strip_quotes(str(ctx.STRING_LITERAL().getText()))