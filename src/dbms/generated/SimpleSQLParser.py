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
        4,1,27,184,2,0,7,0,2,1,7,1,2,2,7,2,2,3,7,3,2,4,7,4,2,5,7,5,2,6,7,
        6,2,7,7,7,2,8,7,8,2,9,7,9,2,10,7,10,2,11,7,11,2,12,7,12,2,13,7,13,
        2,14,7,14,2,15,7,15,2,16,7,16,2,17,7,17,2,18,7,18,2,19,7,19,2,20,
        7,20,1,0,1,0,1,0,1,0,1,0,3,0,48,8,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,
        1,2,1,2,1,2,1,2,1,2,1,2,1,2,1,2,1,2,1,2,1,2,1,3,1,3,1,3,1,3,1,3,
        1,3,3,3,74,8,3,1,4,1,4,1,4,1,4,1,4,1,4,3,4,82,8,4,1,5,1,5,1,5,1,
        5,1,5,3,5,89,8,5,1,6,1,6,3,6,93,8,6,1,7,1,7,1,7,5,7,98,8,7,10,7,
        12,7,101,9,7,1,8,1,8,1,8,1,9,1,9,1,9,5,9,109,8,9,10,9,12,9,112,9,
        9,1,10,1,10,1,11,1,11,1,11,5,11,119,8,11,10,11,12,11,122,9,11,1,
        12,1,12,1,12,1,12,3,12,128,8,12,1,13,1,13,1,14,1,14,1,14,5,14,135,
        8,14,10,14,12,14,138,9,14,1,15,1,15,1,15,5,15,143,8,15,10,15,12,
        15,146,9,15,1,16,1,16,1,16,1,16,1,16,1,16,1,16,1,16,1,16,1,16,1,
        16,1,16,3,16,160,8,16,1,17,1,17,1,17,5,17,165,8,17,10,17,12,17,168,
        9,17,1,18,1,18,1,18,1,18,1,18,1,18,1,18,1,18,3,18,178,8,18,1,19,
        1,19,1,20,1,20,1,20,0,0,21,0,2,4,6,8,10,12,14,16,18,20,22,24,26,
        28,30,32,34,36,38,40,0,1,1,0,19,21,182,0,47,1,0,0,0,2,49,1,0,0,0,
        4,56,1,0,0,0,6,67,1,0,0,0,8,75,1,0,0,0,10,83,1,0,0,0,12,92,1,0,0,
        0,14,94,1,0,0,0,16,102,1,0,0,0,18,105,1,0,0,0,20,113,1,0,0,0,22,
        115,1,0,0,0,24,127,1,0,0,0,26,129,1,0,0,0,28,131,1,0,0,0,30,139,
        1,0,0,0,32,159,1,0,0,0,34,161,1,0,0,0,36,177,1,0,0,0,38,179,1,0,
        0,0,40,181,1,0,0,0,42,48,3,2,1,0,43,48,3,4,2,0,44,48,3,6,3,0,45,
        48,3,8,4,0,46,48,3,10,5,0,47,42,1,0,0,0,47,43,1,0,0,0,47,44,1,0,
        0,0,47,45,1,0,0,0,47,46,1,0,0,0,48,1,1,0,0,0,49,50,5,1,0,0,50,51,
        5,2,0,0,51,52,3,38,19,0,52,53,5,17,0,0,53,54,3,18,9,0,54,55,5,18,
        0,0,55,3,1,0,0,0,56,57,5,3,0,0,57,58,5,4,0,0,58,59,3,38,19,0,59,
        60,5,17,0,0,60,61,3,14,7,0,61,62,5,18,0,0,62,63,5,5,0,0,63,64,5,
        17,0,0,64,65,3,22,11,0,65,66,5,18,0,0,66,5,1,0,0,0,67,68,5,6,0,0,
        68,69,3,12,6,0,69,70,5,7,0,0,70,73,3,38,19,0,71,72,5,8,0,0,72,74,
        3,26,13,0,73,71,1,0,0,0,73,74,1,0,0,0,74,7,1,0,0,0,75,76,5,9,0,0,
        76,77,3,38,19,0,77,78,5,10,0,0,78,81,3,34,17,0,79,80,5,8,0,0,80,
        82,3,26,13,0,81,79,1,0,0,0,81,82,1,0,0,0,82,9,1,0,0,0,83,84,5,11,
        0,0,84,85,5,7,0,0,85,88,3,38,19,0,86,87,5,8,0,0,87,89,3,26,13,0,
        88,86,1,0,0,0,88,89,1,0,0,0,89,11,1,0,0,0,90,93,5,14,0,0,91,93,3,
        14,7,0,92,90,1,0,0,0,92,91,1,0,0,0,93,13,1,0,0,0,94,99,3,38,19,0,
        95,96,5,16,0,0,96,98,3,38,19,0,97,95,1,0,0,0,98,101,1,0,0,0,99,97,
        1,0,0,0,99,100,1,0,0,0,100,15,1,0,0,0,101,99,1,0,0,0,102,103,3,38,
        19,0,103,104,3,20,10,0,104,17,1,0,0,0,105,110,3,16,8,0,106,107,5,
        16,0,0,107,109,3,16,8,0,108,106,1,0,0,0,109,112,1,0,0,0,110,108,
        1,0,0,0,110,111,1,0,0,0,111,19,1,0,0,0,112,110,1,0,0,0,113,114,7,
        0,0,0,114,21,1,0,0,0,115,120,3,24,12,0,116,117,5,16,0,0,117,119,
        3,24,12,0,118,116,1,0,0,0,119,122,1,0,0,0,120,118,1,0,0,0,120,121,
        1,0,0,0,121,23,1,0,0,0,122,120,1,0,0,0,123,128,5,24,0,0,124,128,
        5,22,0,0,125,128,5,23,0,0,126,128,3,40,20,0,127,123,1,0,0,0,127,
        124,1,0,0,0,127,125,1,0,0,0,127,126,1,0,0,0,128,25,1,0,0,0,129,130,
        3,28,14,0,130,27,1,0,0,0,131,136,3,30,15,0,132,133,5,13,0,0,133,
        135,3,30,15,0,134,132,1,0,0,0,135,138,1,0,0,0,136,134,1,0,0,0,136,
        137,1,0,0,0,137,29,1,0,0,0,138,136,1,0,0,0,139,144,3,32,16,0,140,
        141,5,12,0,0,141,143,3,32,16,0,142,140,1,0,0,0,143,146,1,0,0,0,144,
        142,1,0,0,0,144,145,1,0,0,0,145,31,1,0,0,0,146,144,1,0,0,0,147,148,
        5,17,0,0,148,149,3,26,13,0,149,150,5,18,0,0,150,160,1,0,0,0,151,
        152,3,38,19,0,152,153,5,15,0,0,153,154,3,24,12,0,154,160,1,0,0,0,
        155,156,3,38,19,0,156,157,5,15,0,0,157,158,3,38,19,0,158,160,1,0,
        0,0,159,147,1,0,0,0,159,151,1,0,0,0,159,155,1,0,0,0,160,33,1,0,0,
        0,161,166,3,36,18,0,162,163,5,16,0,0,163,165,3,36,18,0,164,162,1,
        0,0,0,165,168,1,0,0,0,166,164,1,0,0,0,166,167,1,0,0,0,167,35,1,0,
        0,0,168,166,1,0,0,0,169,170,3,38,19,0,170,171,5,15,0,0,171,172,3,
        24,12,0,172,178,1,0,0,0,173,174,3,38,19,0,174,175,5,15,0,0,175,176,
        3,38,19,0,176,178,1,0,0,0,177,169,1,0,0,0,177,173,1,0,0,0,178,37,
        1,0,0,0,179,180,5,25,0,0,180,39,1,0,0,0,181,182,5,26,0,0,182,41,
        1,0,0,0,14,47,73,81,88,92,99,110,120,127,136,144,159,166,177
    ]

class SimpleSQLParser ( Parser ):

    grammarFileName = "SimpleSQL.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "'CREATE'", "'TABLE'", "'INSERT'", "'INTO'", 
                     "'VALUES'", "'SELECT'", "'FROM'", "'WHERE'", "'UPDATE'", 
                     "'SET'", "'DELETE'", "'AND'", "'OR'", "'*'", "'='", 
                     "','", "'('", "')'", "'INT'", "'BOOL'", "'TEXT'", "'TRUE'", 
                     "'FALSE'" ]

    symbolicNames = [ "<INVALID>", "CREATE", "TABLE", "INSERT", "INTO", 
                      "VALUES", "SELECT", "FROM", "WHERE", "UPDATE", "SET", 
                      "DELETE", "AND", "OR", "STAR", "EQ", "COMMA", "LPAREN", 
                      "RPAREN", "INT_T", "BOOL_T", "TEXT_T", "TRUE", "FALSE", 
                      "INTEGER_LITERAL", "IDENTIFIER", "STRING_LITERAL", 
                      "WS" ]

    RULE_statement = 0
    RULE_createTable = 1
    RULE_insertInto = 2
    RULE_selectStmt = 3
    RULE_updateStmt = 4
    RULE_deleteStmt = 5
    RULE_selectColumns = 6
    RULE_columnList = 7
    RULE_columnDef = 8
    RULE_columnDefList = 9
    RULE_typeName = 10
    RULE_valueList = 11
    RULE_valueLit = 12
    RULE_whereExpr = 13
    RULE_whereOr = 14
    RULE_whereAnd = 15
    RULE_whereAtom = 16
    RULE_assignmentList = 17
    RULE_assignment = 18
    RULE_identifier = 19
    RULE_stringLiteral = 20

    ruleNames =  [ "statement", "createTable", "insertInto", "selectStmt", 
                   "updateStmt", "deleteStmt", "selectColumns", "columnList", 
                   "columnDef", "columnDefList", "typeName", "valueList", 
                   "valueLit", "whereExpr", "whereOr", "whereAnd", "whereAtom", 
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
    INT_T=19
    BOOL_T=20
    TEXT_T=21
    TRUE=22
    FALSE=23
    INTEGER_LITERAL=24
    IDENTIFIER=25
    STRING_LITERAL=26
    WS=27

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
            self.state = 47
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [1]:
                self.enterOuterAlt(localctx, 1)
                self.state = 42
                self.createTable()
                pass
            elif token in [3]:
                self.enterOuterAlt(localctx, 2)
                self.state = 43
                self.insertInto()
                pass
            elif token in [6]:
                self.enterOuterAlt(localctx, 3)
                self.state = 44
                self.selectStmt()
                pass
            elif token in [9]:
                self.enterOuterAlt(localctx, 4)
                self.state = 45
                self.updateStmt()
                pass
            elif token in [11]:
                self.enterOuterAlt(localctx, 5)
                self.state = 46
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

        def columnDefList(self):
            return self.getTypedRuleContext(SimpleSQLParser.ColumnDefListContext,0)


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
            self.state = 49
            self.match(SimpleSQLParser.CREATE)
            self.state = 50
            self.match(SimpleSQLParser.TABLE)
            self.state = 51
            self.identifier()
            self.state = 52
            self.match(SimpleSQLParser.LPAREN)
            self.state = 53
            self.columnDefList()
            self.state = 54
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
            self.state = 56
            self.match(SimpleSQLParser.INSERT)
            self.state = 57
            self.match(SimpleSQLParser.INTO)
            self.state = 58
            self.identifier()
            self.state = 59
            self.match(SimpleSQLParser.LPAREN)
            self.state = 60
            self.columnList()
            self.state = 61
            self.match(SimpleSQLParser.RPAREN)
            self.state = 62
            self.match(SimpleSQLParser.VALUES)
            self.state = 63
            self.match(SimpleSQLParser.LPAREN)
            self.state = 64
            self.valueList()
            self.state = 65
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
            self.state = 67
            self.match(SimpleSQLParser.SELECT)
            self.state = 68
            self.selectColumns()
            self.state = 69
            self.match(SimpleSQLParser.FROM)
            self.state = 70
            self.identifier()
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
            self.state = 75
            self.match(SimpleSQLParser.UPDATE)
            self.state = 76
            self.identifier()
            self.state = 77
            self.match(SimpleSQLParser.SET)
            self.state = 78
            self.assignmentList()
            self.state = 81
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==8:
                self.state = 79
                self.match(SimpleSQLParser.WHERE)
                self.state = 80
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
            self.state = 83
            self.match(SimpleSQLParser.DELETE)
            self.state = 84
            self.match(SimpleSQLParser.FROM)
            self.state = 85
            self.identifier()
            self.state = 88
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==8:
                self.state = 86
                self.match(SimpleSQLParser.WHERE)
                self.state = 87
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
            self.state = 92
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [14]:
                self.enterOuterAlt(localctx, 1)
                self.state = 90
                self.match(SimpleSQLParser.STAR)
                pass
            elif token in [25]:
                self.enterOuterAlt(localctx, 2)
                self.state = 91
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
            self.state = 94
            self.identifier()
            self.state = 99
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==16:
                self.state = 95
                self.match(SimpleSQLParser.COMMA)
                self.state = 96
                self.identifier()
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


    class ColumnDefContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def identifier(self):
            return self.getTypedRuleContext(SimpleSQLParser.IdentifierContext,0)


        def typeName(self):
            return self.getTypedRuleContext(SimpleSQLParser.TypeNameContext,0)


        def getRuleIndex(self):
            return SimpleSQLParser.RULE_columnDef

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitColumnDef" ):
                return visitor.visitColumnDef(self)
            else:
                return visitor.visitChildren(self)




    def columnDef(self):

        localctx = SimpleSQLParser.ColumnDefContext(self, self._ctx, self.state)
        self.enterRule(localctx, 16, self.RULE_columnDef)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 102
            self.identifier()
            self.state = 103
            self.typeName()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ColumnDefListContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def columnDef(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(SimpleSQLParser.ColumnDefContext)
            else:
                return self.getTypedRuleContext(SimpleSQLParser.ColumnDefContext,i)


        def COMMA(self, i:int=None):
            if i is None:
                return self.getTokens(SimpleSQLParser.COMMA)
            else:
                return self.getToken(SimpleSQLParser.COMMA, i)

        def getRuleIndex(self):
            return SimpleSQLParser.RULE_columnDefList

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitColumnDefList" ):
                return visitor.visitColumnDefList(self)
            else:
                return visitor.visitChildren(self)




    def columnDefList(self):

        localctx = SimpleSQLParser.ColumnDefListContext(self, self._ctx, self.state)
        self.enterRule(localctx, 18, self.RULE_columnDefList)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 105
            self.columnDef()
            self.state = 110
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==16:
                self.state = 106
                self.match(SimpleSQLParser.COMMA)
                self.state = 107
                self.columnDef()
                self.state = 112
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class TypeNameContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def INT_T(self):
            return self.getToken(SimpleSQLParser.INT_T, 0)

        def BOOL_T(self):
            return self.getToken(SimpleSQLParser.BOOL_T, 0)

        def TEXT_T(self):
            return self.getToken(SimpleSQLParser.TEXT_T, 0)

        def getRuleIndex(self):
            return SimpleSQLParser.RULE_typeName

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitTypeName" ):
                return visitor.visitTypeName(self)
            else:
                return visitor.visitChildren(self)




    def typeName(self):

        localctx = SimpleSQLParser.TypeNameContext(self, self._ctx, self.state)
        self.enterRule(localctx, 20, self.RULE_typeName)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 113
            _la = self._input.LA(1)
            if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 3670016) != 0)):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
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

        def valueLit(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(SimpleSQLParser.ValueLitContext)
            else:
                return self.getTypedRuleContext(SimpleSQLParser.ValueLitContext,i)


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
        self.enterRule(localctx, 22, self.RULE_valueList)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 115
            self.valueLit()
            self.state = 120
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==16:
                self.state = 116
                self.match(SimpleSQLParser.COMMA)
                self.state = 117
                self.valueLit()
                self.state = 122
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ValueLitContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def INTEGER_LITERAL(self):
            return self.getToken(SimpleSQLParser.INTEGER_LITERAL, 0)

        def TRUE(self):
            return self.getToken(SimpleSQLParser.TRUE, 0)

        def FALSE(self):
            return self.getToken(SimpleSQLParser.FALSE, 0)

        def stringLiteral(self):
            return self.getTypedRuleContext(SimpleSQLParser.StringLiteralContext,0)


        def getRuleIndex(self):
            return SimpleSQLParser.RULE_valueLit

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitValueLit" ):
                return visitor.visitValueLit(self)
            else:
                return visitor.visitChildren(self)




    def valueLit(self):

        localctx = SimpleSQLParser.ValueLitContext(self, self._ctx, self.state)
        self.enterRule(localctx, 24, self.RULE_valueLit)
        try:
            self.state = 127
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [24]:
                self.enterOuterAlt(localctx, 1)
                self.state = 123
                self.match(SimpleSQLParser.INTEGER_LITERAL)
                pass
            elif token in [22]:
                self.enterOuterAlt(localctx, 2)
                self.state = 124
                self.match(SimpleSQLParser.TRUE)
                pass
            elif token in [23]:
                self.enterOuterAlt(localctx, 3)
                self.state = 125
                self.match(SimpleSQLParser.FALSE)
                pass
            elif token in [26]:
                self.enterOuterAlt(localctx, 4)
                self.state = 126
                self.stringLiteral()
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
        self.enterRule(localctx, 26, self.RULE_whereExpr)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 129
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
        self.enterRule(localctx, 28, self.RULE_whereOr)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 131
            self.whereAnd()
            self.state = 136
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==13:
                self.state = 132
                self.match(SimpleSQLParser.OR)
                self.state = 133
                self.whereAnd()
                self.state = 138
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
        self.enterRule(localctx, 30, self.RULE_whereAnd)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 139
            self.whereAtom()
            self.state = 144
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==12:
                self.state = 140
                self.match(SimpleSQLParser.AND)
                self.state = 141
                self.whereAtom()
                self.state = 146
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

        def valueLit(self):
            return self.getTypedRuleContext(SimpleSQLParser.ValueLitContext,0)


        def getRuleIndex(self):
            return SimpleSQLParser.RULE_whereAtom

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitWhereAtom" ):
                return visitor.visitWhereAtom(self)
            else:
                return visitor.visitChildren(self)




    def whereAtom(self):

        localctx = SimpleSQLParser.WhereAtomContext(self, self._ctx, self.state)
        self.enterRule(localctx, 32, self.RULE_whereAtom)
        try:
            self.state = 159
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,11,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 147
                self.match(SimpleSQLParser.LPAREN)
                self.state = 148
                self.whereExpr()
                self.state = 149
                self.match(SimpleSQLParser.RPAREN)
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 151
                self.identifier()
                self.state = 152
                self.match(SimpleSQLParser.EQ)
                self.state = 153
                self.valueLit()
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 155
                self.identifier()
                self.state = 156
                self.match(SimpleSQLParser.EQ)
                self.state = 157
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
        self.enterRule(localctx, 34, self.RULE_assignmentList)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 161
            self.assignment()
            self.state = 166
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==16:
                self.state = 162
                self.match(SimpleSQLParser.COMMA)
                self.state = 163
                self.assignment()
                self.state = 168
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

        def valueLit(self):
            return self.getTypedRuleContext(SimpleSQLParser.ValueLitContext,0)


        def getRuleIndex(self):
            return SimpleSQLParser.RULE_assignment

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAssignment" ):
                return visitor.visitAssignment(self)
            else:
                return visitor.visitChildren(self)




    def assignment(self):

        localctx = SimpleSQLParser.AssignmentContext(self, self._ctx, self.state)
        self.enterRule(localctx, 36, self.RULE_assignment)
        try:
            self.state = 177
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,13,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 169
                self.identifier()
                self.state = 170
                self.match(SimpleSQLParser.EQ)
                self.state = 171
                self.valueLit()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 173
                self.identifier()
                self.state = 174
                self.match(SimpleSQLParser.EQ)
                self.state = 175
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
        self.enterRule(localctx, 38, self.RULE_identifier)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 179
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
        self.enterRule(localctx, 40, self.RULE_stringLiteral)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 181
            self.match(SimpleSQLParser.STRING_LITERAL)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx





