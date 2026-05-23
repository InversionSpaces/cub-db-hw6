# Generated from grammar/SimpleSQL.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .SimpleSQLParser import SimpleSQLParser
else:
    from SimpleSQLParser import SimpleSQLParser

# This class defines a complete generic visitor for a parse tree produced by SimpleSQLParser.

class SimpleSQLVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by SimpleSQLParser#statement.
    def visitStatement(self, ctx:SimpleSQLParser.StatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SimpleSQLParser#createTable.
    def visitCreateTable(self, ctx:SimpleSQLParser.CreateTableContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SimpleSQLParser#insertInto.
    def visitInsertInto(self, ctx:SimpleSQLParser.InsertIntoContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SimpleSQLParser#selectStmt.
    def visitSelectStmt(self, ctx:SimpleSQLParser.SelectStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SimpleSQLParser#updateStmt.
    def visitUpdateStmt(self, ctx:SimpleSQLParser.UpdateStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SimpleSQLParser#deleteStmt.
    def visitDeleteStmt(self, ctx:SimpleSQLParser.DeleteStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SimpleSQLParser#selectColumns.
    def visitSelectColumns(self, ctx:SimpleSQLParser.SelectColumnsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SimpleSQLParser#columnList.
    def visitColumnList(self, ctx:SimpleSQLParser.ColumnListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SimpleSQLParser#valueList.
    def visitValueList(self, ctx:SimpleSQLParser.ValueListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SimpleSQLParser#whereExpr.
    def visitWhereExpr(self, ctx:SimpleSQLParser.WhereExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SimpleSQLParser#whereOr.
    def visitWhereOr(self, ctx:SimpleSQLParser.WhereOrContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SimpleSQLParser#whereAnd.
    def visitWhereAnd(self, ctx:SimpleSQLParser.WhereAndContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SimpleSQLParser#whereAtom.
    def visitWhereAtom(self, ctx:SimpleSQLParser.WhereAtomContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SimpleSQLParser#assignmentList.
    def visitAssignmentList(self, ctx:SimpleSQLParser.AssignmentListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SimpleSQLParser#assignment.
    def visitAssignment(self, ctx:SimpleSQLParser.AssignmentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SimpleSQLParser#identifier.
    def visitIdentifier(self, ctx:SimpleSQLParser.IdentifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SimpleSQLParser#stringLiteral.
    def visitStringLiteral(self, ctx:SimpleSQLParser.StringLiteralContext):
        return self.visitChildren(ctx)



del SimpleSQLParser