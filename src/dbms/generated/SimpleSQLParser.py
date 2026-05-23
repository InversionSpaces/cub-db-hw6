# Generated from grammar/SimpleSQL.g4 by ANTLR 4.13.2
# encoding: utf-8
from antlr4 import *
from io import StringIO
import sys
if sys.version_info[1] > 5:
	from typing import TextIO
else:
	from typing.io import TextIO

def serializedATN():
    return [
        4,1,21,157,2,0,7,0,2,1,7,1,2,2,7,2,2,3,7,3,2,4,7,4,2,5,7,5,2,6,7,
        6,2,7,7,7,2,8,7,8,2,9,7,9,2,10,7,10,2,11,7,11,2,12,7,12,2,13,7,13,
        2,14,7,14,2,15,7,15,2,16,7,16,1,0,1,0,1,0,1,0,1,0,3,0,40,8,0,1,1,
        1,1,1,1,1,1,1,1,1,1,1,1,1,2,1,2,1,2,1,2,1,2,1,2,1,2,1,2,1,2,1,2,
        1,2,1,3,1,3,1,3,1,3,1,3,1,3,3,3,66,8,3,1,4,1,4,1,4,1,4,1,4,1,4,3,
        4,74,8,4,1,5,1,5,1,5,1,5,1,5,3,5,81,8,5,1,6,1,6,3,6,85,8,6,1,7,1,
        7,1,7,5,7,90,8,7,10,7,12,7,93,9,7,1,8,1,8,1,8,5,8,98,8,8,10,8,12,
        8,101,9,8,1,9,1,9,1,10,1,10,1,10,5,10,108,8,10,10,10,12,10,111,9,
        10,1,11,1,11,1,11,5,11,116,8,11,10,11,12,11,119,9,11,1,12,1,12,1,
        12,1,12,1,12,1,12,1,12,1,12,1,12,1,12,1,12,1,12,3,12,133,8,12,1,
        13,1,13,1,13,5,13,138,8,13,10,13,12,13,141,9,13,1,14,1,14,1,14,1,
        14,1,14,1,14,1,14,1,14,3,14,151,8,14,1,15,1,15,1,16,1,16,1,16,0,
        0,17,0,2,4,6,8,10,12,14,16,18,20,22,24,26,28,30,32,0,0,155,0,39,
        1,0,0,0,2,41,1,0,0,0,4,48,1,0,0,0,6,59,1,0,0,0,8,67,1,0,0,0,10,75,
        1,0,0,0,12,84,1,0,0,0,14,86,1,0,0,0,16,94,1,0,0,0,18,102,1,0,0,0,
        20,104,1,0,0,0,22,112,1,0,0,0,24,132,1,0,0,0,26,134,1,0,0,0,28,150,
        1,0,0,0,30,152,1,0,0,0,32,154,1,0,0,0,34,40,3,2,1,0,35,40,3,4,2,
        0,36,40,3,6,3,0,37,40,3,8,4,0,38,40,3,10,5,0,39,34,1,0,0,0,39,35,
        1,0,0,0,39,36,1,0,0,0,39,37,1,0,0,0,39,38,1,0,0,0,40,1,1,0,0,0,41,
        42,5,1,0,0,42,43,5,2,0,0,43,44,3,30,15,0,44,45,5,17,0,0,45,46,3,
        14,7,0,46,47,5,18,0,0,47,3,1,0,0,0,48,49,5,3,0,0,49,50,5,4,0,0,50,
        51,3,30,15,0,51,52,5,17,0,0,52,53,3,14,7,0,53,54,5,18,0,0,54,55,
        5,5,0,0,55,56,5,17,0,0,56,57,3,16,8,0,57,58,5,18,0,0,58,5,1,0,0,
        0,59,60,5,6,0,0,60,61,3,12,6,0,61,62,5,7,0,0,62,65,3,30,15,0,63,
        64,5,8,0,0,64,66,3,18,9,0,65,63,1,0,0,0,65,66,1,0,0,0,66,7,1,0,0,
        0,67,68,5,9,0,0,68,69,3,30,15,0,69,70,5,10,0,0,70,73,3,26,13,0,71,
        72,5,8,0,0,72,74,3,18,9,0,73,71,1,0,0,0,73,74,1,0,0,0,74,9,1,0,0,
        0,75,76,5,11,0,0,76,77,5,7,0,0,77,80,3,30,15,0,78,79,5,8,0,0,79,
        81,3,18,9,0,80,78,1,0,0,0,80,81,1,0,0,0,81,11,1,0,0,0,82,85,5,14,
        0,0,83,85,3,14,7,0,84,82,1,0,0,0,84,83,1,0,0,0,85,13,1,0,0,0,86,
        91,3,30,15,0,87,88,5,16,0,0,88,90,3,30,15,0,89,87,1,0,0,0,90,93,
        1,0,0,0,91,89,1,0,0,0,91,92,1,0,0,0,92,15,1,0,0,0,93,91,1,0,0,0,
        94,99,3,32,16,0,95,96,5,16,0,0,96,98,3,32,16,0,97,95,1,0,0,0,98,
        101,1,0,0,0,99,97,1,0,0,0,99,100,1,0,0,0,100,17,1,0,0,0,101,99,1,
        0,0,0,102,103,3,20,10,0,103,19,1,0,0,0,104,109,3,22,11,0,105,106,
        5,13,0,0,106,108,3,22,11,0,107,105,1,0,0,0,108,111,1,0,0,0,109,107,
        1,0,0,0,109,110,1,0,0,0,110,21,1,0,0,0,111,109,1,0,0,0,112,117,3,
        24,12,0,113,114,5,12,0,0,114,116,3,24,12,0,115,113,1,0,0,0,116,119,
        1,0,0,0,117,115,1,0,0,0,117,118,1,0,0,0,118,23,1,0,0,0,119,117,1,
        0,0,0,120,121,5,17,0,0,121,122,3,18,9,0,122,123,5,18,0,0,123,133,
        1,0,0,0,124,125,3,30,15,0,125,126,5,15,0,0,126,127,3,32,16,0,127,
        133,1,0,0,0,128,129,3,30,15,0,129,130,5,15,0,0,130,131,3,30,15,0,
        131,133,1,0,0,0,132,120,1,0,0,0,132,124,1,0,0,0,132,128,1,0,0,0,
        133,25,1,0,0,0,134,139,3,28,14,0,135,136,5,16,0,0,136,138,3,28,14,
        0,137,135,1,0,0,0,138,141,1,0,0,0,139,137,1,0,0,0,139,140,1,0,0,
        0,140,27,1,0,0,0,141,139,1,0,0,0,142,143,3,30,15,0,143,144,5,15,
        0,0,144,145,3,32,16,0,145,151,1,0,0,0,146,147,3,30,15,0,147,148,
        5,15,0,0,148,149,3,30,15,0,149,151,1,0,0,0,150,142,1,0,0,0,150,146,
        1,0,0,0,151,29,1,0,0,0,152,153,5,19,0,0,153,31,1,0,0,0,154,155,5,
        20,0,0,155,33,1,0,0,0,12,39,65,73,80,84,91,99,109,117,132,139,150
    ]

class SimpleSQLParser ( Parser ):

    grammarFileName = "SimpleSQL.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "'CREATE'", "'TABLE'", "'INSERT'", "'INTO'", 
                     "'VALUES'", "'SELECT'", "'FROM'", "'WHERE'", "'UPDATE'", 
                     "'SET'", "'DELETE'", "'AND'", "'OR'", "'*'", "'='", 
                     "','", "'('", "')'" ]

    symbolicNames = [ "<INVALID>", "CREATE", "TABLE", "INSERT", "INTO", 
                      "VALUES", "SELECT", "FROM", "WHERE", "UPDATE", "SET", 
                      "DELETE", "AND", "OR", "STAR", "EQ", "COMMA", "LPAREN", 
                      "RPAREN", "IDENTIFIER", "STRING_LITERAL", "WS" ]

    RULE_statement = 0
    RULE_createTable = 1
    RULE_insertInto = 2
    RULE_selectStmt = 3
    RULE_updateStmt = 4
    RULE_deleteStmt = 5
    RULE_selectColumns = 6
    RULE_columnList = 7
    RULE_valueList = 8
    RULE_whereExpr = 9
    RULE_whereOr = 10
    RULE_whereAnd = 11
    RULE_whereAtom = 12
    RULE_assignmentList = 13
    RULE_assignment = 14
    RULE_identifier = 15
    RULE_stringLiteral = 16

    ruleNames =  [ "statement", "createTable", "insertInto", "selectStmt", 
                   "updateStmt", "deleteStmt", "selectColumns", "columnList", 
                   "valueList", "whereExpr", "whereOr", "whereAnd", "whereAtom", 
                   "assignmentList", "assignment", "identifier", "stringLiteral" ]

    EOF = Token.EOF
    CREATE=1
    TABLE=2
    INSERT=3
    INTO=4
    VALUES=5
    SELECT=6
    FROM=7
    WHERE=8
    UPDATE=9
    SET=10
    DELETE=11
    AND=12
    OR=13
    STAR=14
    EQ=15
    COMMA=16
    LPAREN=17
    RPAREN=18
    IDENTIFIER=19
    STRING_LITERAL=20
    WS=21

    def __init__(self, input:TokenStream, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.13.2")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None




    class StatementContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def createTable(self):
            return self.getTypedRuleContext(SimpleSQLParser.CreateTableContext,0)


        def insertInto(self):
            return self.getTypedRuleContext(SimpleSQLParser.InsertIntoContext,0)


        def selectStmt(self):
            return self.getTypedRuleContext(SimpleSQLParser.SelectStmtContext,0)


        def updateStmt(self):
            return self.getTypedRuleContext(SimpleSQLParser.UpdateStmtContext,0)


        def deleteStmt(self):
            return self.getTypedRuleContext(SimpleSQLParser.DeleteStmtContext,0)


        def getRuleIndex(self):
            return SimpleSQLParser.RULE_statement

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitStatement" ):
                return visitor.visitStatement(self)
            else:
                return visitor.visitChildren(self)




    def statement(self):

        localctx = SimpleSQLParser.StatementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_statement)
        try:
            self.state = 39
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [1]:
                self.enterOuterAlt(localctx, 1)
                self.state = 34
                self.createTable()
                pass
            elif token in [3]:
                self.enterOuterAlt(localctx, 2)
                self.state = 35
                self.insertInto()
                pass
            elif token in [6]:
                self.enterOuterAlt(localctx, 3)
                self.state = 36
                self.selectStmt()
                pass
            elif token in [9]:
                self.enterOuterAlt(localctx, 4)
                self.state = 37
                self.updateStmt()
                pass
            elif token in [11]:
                self.enterOuterAlt(localctx, 5)
                self.state = 38
                self.deleteStmt()
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class CreateTableContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def CREATE(self):
            return self.getToken(SimpleSQLParser.CREATE, 0)

        def TABLE(self):
            return self.getToken(SimpleSQLParser.TABLE, 0)

        def identifier(self):
            return self.getTypedRuleContext(SimpleSQLParser.IdentifierContext,0)


        def LPAREN(self):
            return self.getToken(SimpleSQLParser.LPAREN, 0)

        def columnList(self):
            return self.getTypedRuleContext(SimpleSQLParser.ColumnListContext,0)


        def RPAREN(self):
            return self.getToken(SimpleSQLParser.RPAREN, 0)

        def getRuleIndex(self):
            return SimpleSQLParser.RULE_createTable

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitCreateTable" ):
                return visitor.visitCreateTable(self)
            else:
                return visitor.visitChildren(self)




    def createTable(self):

        localctx = SimpleSQLParser.CreateTableContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_createTable)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 41
            self.match(SimpleSQLParser.CREATE)
            self.state = 42
            self.match(SimpleSQLParser.TABLE)
            self.state = 43
            self.identifier()
            self.state = 44
            self.match(SimpleSQLParser.LPAREN)
            self.state = 45
            self.columnList()
            self.state = 46
            self.match(SimpleSQLParser.RPAREN)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class InsertIntoContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def INSERT(self):
            return self.getToken(SimpleSQLParser.INSERT, 0)

        def INTO(self):
            return self.getToken(SimpleSQLParser.INTO, 0)

        def identifier(self):
            return self.getTypedRuleContext(SimpleSQLParser.IdentifierContext,0)


        def LPAREN(self, i:int=None):
            if i is None:
                return self.getTokens(SimpleSQLParser.LPAREN)
            else:
                return self.getToken(SimpleSQLParser.LPAREN, i)

        def columnList(self):
            return self.getTypedRuleContext(SimpleSQLParser.ColumnListContext,0)


        def RPAREN(self, i:int=None):
            if i is None:
                return self.getTokens(SimpleSQLParser.RPAREN)
            else:
                return self.getToken(SimpleSQLParser.RPAREN, i)

        def VALUES(self):
            return self.getToken(SimpleSQLParser.VALUES, 0)

        def valueList(self):
            return self.getTypedRuleContext(SimpleSQLParser.ValueListContext,0)


        def getRuleIndex(self):
            return SimpleSQLParser.RULE_insertInto

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitInsertInto" ):
                return visitor.visitInsertInto(self)
            else:
                return visitor.visitChildren(self)




    def insertInto(self):

        localctx = SimpleSQLParser.InsertIntoContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_insertInto)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 48
            self.match(SimpleSQLParser.INSERT)
            self.state = 49
            self.match(SimpleSQLParser.INTO)
            self.state = 50
            self.identifier()
            self.state = 51
            self.match(SimpleSQLParser.LPAREN)
            self.state = 52
            self.columnList()
            self.state = 53
            self.match(SimpleSQLParser.RPAREN)
            self.state = 54
            self.match(SimpleSQLParser.VALUES)
            self.state = 55
            self.match(SimpleSQLParser.LPAREN)
            self.state = 56
            self.valueList()
            self.state = 57
            self.match(SimpleSQLParser.RPAREN)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class SelectStmtContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def SELECT(self):
            return self.getToken(SimpleSQLParser.SELECT, 0)

        def selectColumns(self):
            return self.getTypedRuleContext(SimpleSQLParser.SelectColumnsContext,0)


        def FROM(self):
            return self.getToken(SimpleSQLParser.FROM, 0)

        def identifier(self):
            return self.getTypedRuleContext(SimpleSQLParser.IdentifierContext,0)


        def WHERE(self):
            return self.getToken(SimpleSQLParser.WHERE, 0)

        def whereExpr(self):
            return self.getTypedRuleContext(SimpleSQLParser.WhereExprContext,0)


        def getRuleIndex(self):
            return SimpleSQLParser.RULE_selectStmt

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitSelectStmt" ):
                return visitor.visitSelectStmt(self)
            else:
                return visitor.visitChildren(self)




    def selectStmt(self):

        localctx = SimpleSQLParser.SelectStmtContext(self, self._ctx, self.state)
        self.enterRule(localctx, 6, self.RULE_selectStmt)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 59
            self.match(SimpleSQLParser.SELECT)
            self.state = 60
            self.selectColumns()
            self.state = 61
            self.match(SimpleSQLParser.FROM)
            self.state = 62
            self.identifier()
            self.state = 65
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==8:
                self.state = 63
                self.match(SimpleSQLParser.WHERE)
                self.state = 64
                self.whereExpr()


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class UpdateStmtContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def UPDATE(self):
            return self.getToken(SimpleSQLParser.UPDATE, 0)

        def identifier(self):
            return self.getTypedRuleContext(SimpleSQLParser.IdentifierContext,0)


        def SET(self):
            return self.getToken(SimpleSQLParser.SET, 0)

        def assignmentList(self):
            return self.getTypedRuleContext(SimpleSQLParser.AssignmentListContext,0)


        def WHERE(self):
            return self.getToken(SimpleSQLParser.WHERE, 0)

        def whereExpr(self):
            return self.getTypedRuleContext(SimpleSQLParser.WhereExprContext,0)


        def getRuleIndex(self):
            return SimpleSQLParser.RULE_updateStmt

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitUpdateStmt" ):
                return visitor.visitUpdateStmt(self)
            else:
                return visitor.visitChildren(self)




    def updateStmt(self):

        localctx = SimpleSQLParser.UpdateStmtContext(self, self._ctx, self.state)
        self.enterRule(localctx, 8, self.RULE_updateStmt)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 67
            self.match(SimpleSQLParser.UPDATE)
            self.state = 68
            self.identifier()
            self.state = 69
            self.match(SimpleSQLParser.SET)
            self.state = 70
            self.assignmentList()
            self.state = 73
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==8:
                self.state = 71
                self.match(SimpleSQLParser.WHERE)
                self.state = 72
                self.whereExpr()


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class DeleteStmtContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def DELETE(self):
            return self.getToken(SimpleSQLParser.DELETE, 0)

        def FROM(self):
            return self.getToken(SimpleSQLParser.FROM, 0)

        def identifier(self):
            return self.getTypedRuleContext(SimpleSQLParser.IdentifierContext,0)


        def WHERE(self):
            return self.getToken(SimpleSQLParser.WHERE, 0)

        def whereExpr(self):
            return self.getTypedRuleContext(SimpleSQLParser.WhereExprContext,0)


        def getRuleIndex(self):
            return SimpleSQLParser.RULE_deleteStmt

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitDeleteStmt" ):
                return visitor.visitDeleteStmt(self)
            else:
                return visitor.visitChildren(self)




    def deleteStmt(self):

        localctx = SimpleSQLParser.DeleteStmtContext(self, self._ctx, self.state)
        self.enterRule(localctx, 10, self.RULE_deleteStmt)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 75
            self.match(SimpleSQLParser.DELETE)
            self.state = 76
            self.match(SimpleSQLParser.FROM)
            self.state = 77
            self.identifier()
            self.state = 80
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==8:
                self.state = 78
                self.match(SimpleSQLParser.WHERE)
                self.state = 79
                self.whereExpr()


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class SelectColumnsContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def STAR(self):
            return self.getToken(SimpleSQLParser.STAR, 0)

        def columnList(self):
            return self.getTypedRuleContext(SimpleSQLParser.ColumnListContext,0)


        def getRuleIndex(self):
            return SimpleSQLParser.RULE_selectColumns

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitSelectColumns" ):
                return visitor.visitSelectColumns(self)
            else:
                return visitor.visitChildren(self)




    def selectColumns(self):

        localctx = SimpleSQLParser.SelectColumnsContext(self, self._ctx, self.state)
        self.enterRule(localctx, 12, self.RULE_selectColumns)
        try:
            self.state = 84
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [14]:
                self.enterOuterAlt(localctx, 1)
                self.state = 82
                self.match(SimpleSQLParser.STAR)
                pass
            elif token in [19]:
                self.enterOuterAlt(localctx, 2)
                self.state = 83
                self.columnList()
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ColumnListContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def identifier(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(SimpleSQLParser.IdentifierContext)
            else:
                return self.getTypedRuleContext(SimpleSQLParser.IdentifierContext,i)


        def COMMA(self, i:int=None):
            if i is None:
                return self.getTokens(SimpleSQLParser.COMMA)
            else:
                return self.getToken(SimpleSQLParser.COMMA, i)

        def getRuleIndex(self):
            return SimpleSQLParser.RULE_columnList

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitColumnList" ):
                return visitor.visitColumnList(self)
            else:
                return visitor.visitChildren(self)




    def columnList(self):

        localctx = SimpleSQLParser.ColumnListContext(self, self._ctx, self.state)
        self.enterRule(localctx, 14, self.RULE_columnList)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 86
            self.identifier()
            self.state = 91
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==16:
                self.state = 87
                self.match(SimpleSQLParser.COMMA)
                self.state = 88
                self.identifier()
                self.state = 93
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ValueListContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def stringLiteral(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(SimpleSQLParser.StringLiteralContext)
            else:
                return self.getTypedRuleContext(SimpleSQLParser.StringLiteralContext,i)


        def COMMA(self, i:int=None):
            if i is None:
                return self.getTokens(SimpleSQLParser.COMMA)
            else:
                return self.getToken(SimpleSQLParser.COMMA, i)

        def getRuleIndex(self):
            return SimpleSQLParser.RULE_valueList

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitValueList" ):
                return visitor.visitValueList(self)
            else:
                return visitor.visitChildren(self)




    def valueList(self):

        localctx = SimpleSQLParser.ValueListContext(self, self._ctx, self.state)
        self.enterRule(localctx, 16, self.RULE_valueList)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 94
            self.stringLiteral()
            self.state = 99
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==16:
                self.state = 95
                self.match(SimpleSQLParser.COMMA)
                self.state = 96
                self.stringLiteral()
                self.state = 101
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class WhereExprContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def whereOr(self):
            return self.getTypedRuleContext(SimpleSQLParser.WhereOrContext,0)


        def getRuleIndex(self):
            return SimpleSQLParser.RULE_whereExpr

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitWhereExpr" ):
                return visitor.visitWhereExpr(self)
            else:
                return visitor.visitChildren(self)




    def whereExpr(self):

        localctx = SimpleSQLParser.WhereExprContext(self, self._ctx, self.state)
        self.enterRule(localctx, 18, self.RULE_whereExpr)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 102
            self.whereOr()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class WhereOrContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def whereAnd(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(SimpleSQLParser.WhereAndContext)
            else:
                return self.getTypedRuleContext(SimpleSQLParser.WhereAndContext,i)


        def OR(self, i:int=None):
            if i is None:
                return self.getTokens(SimpleSQLParser.OR)
            else:
                return self.getToken(SimpleSQLParser.OR, i)

        def getRuleIndex(self):
            return SimpleSQLParser.RULE_whereOr

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitWhereOr" ):
                return visitor.visitWhereOr(self)
            else:
                return visitor.visitChildren(self)




    def whereOr(self):

        localctx = SimpleSQLParser.WhereOrContext(self, self._ctx, self.state)
        self.enterRule(localctx, 20, self.RULE_whereOr)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 104
            self.whereAnd()
            self.state = 109
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==13:
                self.state = 105
                self.match(SimpleSQLParser.OR)
                self.state = 106
                self.whereAnd()
                self.state = 111
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class WhereAndContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def whereAtom(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(SimpleSQLParser.WhereAtomContext)
            else:
                return self.getTypedRuleContext(SimpleSQLParser.WhereAtomContext,i)


        def AND(self, i:int=None):
            if i is None:
                return self.getTokens(SimpleSQLParser.AND)
            else:
                return self.getToken(SimpleSQLParser.AND, i)

        def getRuleIndex(self):
            return SimpleSQLParser.RULE_whereAnd

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitWhereAnd" ):
                return visitor.visitWhereAnd(self)
            else:
                return visitor.visitChildren(self)




    def whereAnd(self):

        localctx = SimpleSQLParser.WhereAndContext(self, self._ctx, self.state)
        self.enterRule(localctx, 22, self.RULE_whereAnd)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 112
            self.whereAtom()
            self.state = 117
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==12:
                self.state = 113
                self.match(SimpleSQLParser.AND)
                self.state = 114
                self.whereAtom()
                self.state = 119
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class WhereAtomContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def LPAREN(self):
            return self.getToken(SimpleSQLParser.LPAREN, 0)

        def whereExpr(self):
            return self.getTypedRuleContext(SimpleSQLParser.WhereExprContext,0)


        def RPAREN(self):
            return self.getToken(SimpleSQLParser.RPAREN, 0)

        def identifier(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(SimpleSQLParser.IdentifierContext)
            else:
                return self.getTypedRuleContext(SimpleSQLParser.IdentifierContext,i)


        def EQ(self):
            return self.getToken(SimpleSQLParser.EQ, 0)

        def stringLiteral(self):
            return self.getTypedRuleContext(SimpleSQLParser.StringLiteralContext,0)


        def getRuleIndex(self):
            return SimpleSQLParser.RULE_whereAtom

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitWhereAtom" ):
                return visitor.visitWhereAtom(self)
            else:
                return visitor.visitChildren(self)




    def whereAtom(self):

        localctx = SimpleSQLParser.WhereAtomContext(self, self._ctx, self.state)
        self.enterRule(localctx, 24, self.RULE_whereAtom)
        try:
            self.state = 132
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,9,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 120
                self.match(SimpleSQLParser.LPAREN)
                self.state = 121
                self.whereExpr()
                self.state = 122
                self.match(SimpleSQLParser.RPAREN)
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 124
                self.identifier()
                self.state = 125
                self.match(SimpleSQLParser.EQ)
                self.state = 126
                self.stringLiteral()
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 128
                self.identifier()
                self.state = 129
                self.match(SimpleSQLParser.EQ)
                self.state = 130
                self.identifier()
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class AssignmentListContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def assignment(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(SimpleSQLParser.AssignmentContext)
            else:
                return self.getTypedRuleContext(SimpleSQLParser.AssignmentContext,i)


        def COMMA(self, i:int=None):
            if i is None:
                return self.getTokens(SimpleSQLParser.COMMA)
            else:
                return self.getToken(SimpleSQLParser.COMMA, i)

        def getRuleIndex(self):
            return SimpleSQLParser.RULE_assignmentList

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAssignmentList" ):
                return visitor.visitAssignmentList(self)
            else:
                return visitor.visitChildren(self)




    def assignmentList(self):

        localctx = SimpleSQLParser.AssignmentListContext(self, self._ctx, self.state)
        self.enterRule(localctx, 26, self.RULE_assignmentList)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 134
            self.assignment()
            self.state = 139
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==16:
                self.state = 135
                self.match(SimpleSQLParser.COMMA)
                self.state = 136
                self.assignment()
                self.state = 141
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class AssignmentContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def identifier(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(SimpleSQLParser.IdentifierContext)
            else:
                return self.getTypedRuleContext(SimpleSQLParser.IdentifierContext,i)


        def EQ(self):
            return self.getToken(SimpleSQLParser.EQ, 0)

        def stringLiteral(self):
            return self.getTypedRuleContext(SimpleSQLParser.StringLiteralContext,0)


        def getRuleIndex(self):
            return SimpleSQLParser.RULE_assignment

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAssignment" ):
                return visitor.visitAssignment(self)
            else:
                return visitor.visitChildren(self)




    def assignment(self):

        localctx = SimpleSQLParser.AssignmentContext(self, self._ctx, self.state)
        self.enterRule(localctx, 28, self.RULE_assignment)
        try:
            self.state = 150
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,11,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 142
                self.identifier()
                self.state = 143
                self.match(SimpleSQLParser.EQ)
                self.state = 144
                self.stringLiteral()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 146
                self.identifier()
                self.state = 147
                self.match(SimpleSQLParser.EQ)
                self.state = 148
                self.identifier()
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class IdentifierContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def IDENTIFIER(self):
            return self.getToken(SimpleSQLParser.IDENTIFIER, 0)

        def getRuleIndex(self):
            return SimpleSQLParser.RULE_identifier

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitIdentifier" ):
                return visitor.visitIdentifier(self)
            else:
                return visitor.visitChildren(self)




    def identifier(self):

        localctx = SimpleSQLParser.IdentifierContext(self, self._ctx, self.state)
        self.enterRule(localctx, 30, self.RULE_identifier)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 152
            self.match(SimpleSQLParser.IDENTIFIER)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class StringLiteralContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def STRING_LITERAL(self):
            return self.getToken(SimpleSQLParser.STRING_LITERAL, 0)

        def getRuleIndex(self):
            return SimpleSQLParser.RULE_stringLiteral

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitStringLiteral" ):
                return visitor.visitStringLiteral(self)
            else:
                return visitor.visitChildren(self)




    def stringLiteral(self):

        localctx = SimpleSQLParser.StringLiteralContext(self, self._ctx, self.state)
        self.enterRule(localctx, 32, self.RULE_stringLiteral)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 154
            self.match(SimpleSQLParser.STRING_LITERAL)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx





