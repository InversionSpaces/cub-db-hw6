# Generated from grammar/SimpleSQL.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .SimpleSQLParser import SimpleSQLParser
else:
    from SimpleSQLParser import SimpleSQLParser

# This class defines a complete listener for a parse tree produced by SimpleSQLParser.
class SimpleSQLListener(ParseTreeListener):

    # Enter a parse tree produced by SimpleSQLParser#statement.
    def enterStatement(self, ctx:SimpleSQLParser.StatementContext):
        pass

    # Exit a parse tree produced by SimpleSQLParser#statement.
    def exitStatement(self, ctx:SimpleSQLParser.StatementContext):
        pass


    # Enter a parse tree produced by SimpleSQLParser#createTable.
    def enterCreateTable(self, ctx:SimpleSQLParser.CreateTableContext):
        pass

    # Exit a parse tree produced by SimpleSQLParser#createTable.
    def exitCreateTable(self, ctx:SimpleSQLParser.CreateTableContext):
        pass


    # Enter a parse tree produced by SimpleSQLParser#insertInto.
    def enterInsertInto(self, ctx:SimpleSQLParser.InsertIntoContext):
        pass

    # Exit a parse tree produced by SimpleSQLParser#insertInto.
    def exitInsertInto(self, ctx:SimpleSQLParser.InsertIntoContext):
        pass


    # Enter a parse tree produced by SimpleSQLParser#selectStmt.
    def enterSelectStmt(self, ctx:SimpleSQLParser.SelectStmtContext):
        pass

    # Exit a parse tree produced by SimpleSQLParser#selectStmt.
    def exitSelectStmt(self, ctx:SimpleSQLParser.SelectStmtContext):
        pass


    # Enter a parse tree produced by SimpleSQLParser#updateStmt.
    def enterUpdateStmt(self, ctx:SimpleSQLParser.UpdateStmtContext):
        pass

    # Exit a parse tree produced by SimpleSQLParser#updateStmt.
    def exitUpdateStmt(self, ctx:SimpleSQLParser.UpdateStmtContext):
        pass


    # Enter a parse tree produced by SimpleSQLParser#deleteStmt.
    def enterDeleteStmt(self, ctx:SimpleSQLParser.DeleteStmtContext):
        pass

    # Exit a parse tree produced by SimpleSQLParser#deleteStmt.
    def exitDeleteStmt(self, ctx:SimpleSQLParser.DeleteStmtContext):
        pass


    # Enter a parse tree produced by SimpleSQLParser#selectColumns.
    def enterSelectColumns(self, ctx:SimpleSQLParser.SelectColumnsContext):
        pass

    # Exit a parse tree produced by SimpleSQLParser#selectColumns.
    def exitSelectColumns(self, ctx:SimpleSQLParser.SelectColumnsContext):
        pass


    # Enter a parse tree produced by SimpleSQLParser#columnList.
    def enterColumnList(self, ctx:SimpleSQLParser.ColumnListContext):
        pass

    # Exit a parse tree produced by SimpleSQLParser#columnList.
    def exitColumnList(self, ctx:SimpleSQLParser.ColumnListContext):
        pass


    # Enter a parse tree produced by SimpleSQLParser#valueList.
    def enterValueList(self, ctx:SimpleSQLParser.ValueListContext):
        pass

    # Exit a parse tree produced by SimpleSQLParser#valueList.
    def exitValueList(self, ctx:SimpleSQLParser.ValueListContext):
        pass


    # Enter a parse tree produced by SimpleSQLParser#whereExpr.
    def enterWhereExpr(self, ctx:SimpleSQLParser.WhereExprContext):
        pass

    # Exit a parse tree produced by SimpleSQLParser#whereExpr.
    def exitWhereExpr(self, ctx:SimpleSQLParser.WhereExprContext):
        pass


    # Enter a parse tree produced by SimpleSQLParser#whereAtom.
    def enterWhereAtom(self, ctx:SimpleSQLParser.WhereAtomContext):
        pass

    # Exit a parse tree produced by SimpleSQLParser#whereAtom.
    def exitWhereAtom(self, ctx:SimpleSQLParser.WhereAtomContext):
        pass


    # Enter a parse tree produced by SimpleSQLParser#assignmentList.
    def enterAssignmentList(self, ctx:SimpleSQLParser.AssignmentListContext):
        pass

    # Exit a parse tree produced by SimpleSQLParser#assignmentList.
    def exitAssignmentList(self, ctx:SimpleSQLParser.AssignmentListContext):
        pass


    # Enter a parse tree produced by SimpleSQLParser#assignment.
    def enterAssignment(self, ctx:SimpleSQLParser.AssignmentContext):
        pass

    # Exit a parse tree produced by SimpleSQLParser#assignment.
    def exitAssignment(self, ctx:SimpleSQLParser.AssignmentContext):
        pass


    # Enter a parse tree produced by SimpleSQLParser#identifier.
    def enterIdentifier(self, ctx:SimpleSQLParser.IdentifierContext):
        pass

    # Exit a parse tree produced by SimpleSQLParser#identifier.
    def exitIdentifier(self, ctx:SimpleSQLParser.IdentifierContext):
        pass


    # Enter a parse tree produced by SimpleSQLParser#stringLiteral.
    def enterStringLiteral(self, ctx:SimpleSQLParser.StringLiteralContext):
        pass

    # Exit a parse tree produced by SimpleSQLParser#stringLiteral.
    def exitStringLiteral(self, ctx:SimpleSQLParser.StringLiteralContext):
        pass



del SimpleSQLParser