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
        4,1,27,197,2,0,7,0,2,1,7,1,2,2,7,2,2,3,7,3,2,4,7,4,2,5,7,5,2,6,7,
        6,2,7,7,7,2,8,7,8,2,9,7,9,2,10,7,10,2,11,7,11,2,12,7,12,2,13,7,13,
        2,14,7,14,2,15,7,15,2,16,7,16,2,17,7,17,2,18,7,18,2,19,7,19,2,20,
        7,20,2,21,7,21,1,0,1,0,1,0,1,0,1,0,3,0,50,8,0,1,1,1,1,1,1,1,1,1,
        1,1,1,1,1,1,2,1,2,1,2,1,2,1,2,1,2,1,2,1,2,1,2,1,3,1,3,1,3,1,3,1,
        3,1,3,1,3,1,3,5,3,76,8,3,10,3,12,3,79,9,3,1,4,1,4,1,4,1,4,1,4,1,
        4,3,4,87,8,4,1,5,1,5,1,5,1,5,1,5,1,5,3,5,95,8,5,1,6,1,6,1,6,1,6,
        1,6,3,6,102,8,6,1,7,1,7,3,7,106,8,7,1,8,1,8,1,8,5,8,111,8,8,10,8,
        12,8,114,9,8,1,9,1,9,1,9,1,10,1,10,1,10,5,10,122,8,10,10,10,12,10,
        125,9,10,1,11,1,11,1,12,1,12,1,12,5,12,132,8,12,10,12,12,12,135,
        9,12,1,13,1,13,1,13,1,13,3,13,141,8,13,1,14,1,14,1,15,1,15,1,15,
        5,15,148,8,15,10,15,12,15,151,9,15,1,16,1,16,1,16,5,16,156,8,16,
        10,16,12,16,159,9,16,1,17,1,17,1,17,1,17,1,17,1,17,1,17,1,17,1,17,
        1,17,1,17,1,17,3,17,173,8,17,1,18,1,18,1,18,5,18,178,8,18,10,18,
        12,18,181,9,18,1,19,1,19,1,19,1,19,1,19,1,19,1,19,1,19,3,19,191,
        8,19,1,20,1,20,1,21,1,21,1,21,0,0,22,0,2,4,6,8,10,12,14,16,18,20,
        22,24,26,28,30,32,34,36,38,40,42,0,1,1,0,19,21,195,0,49,1,0,0,0,
        2,51,1,0,0,0,4,58,1,0,0,0,6,67,1,0,0,0,8,80,1,0,0,0,10,88,1,0,0,
        0,12,96,1,0,0,0,14,105,1,0,0,0,16,107,1,0,0,0,18,115,1,0,0,0,20,
        118,1,0,0,0,22,126,1,0,0,0,24,128,1,0,0,0,26,140,1,0,0,0,28,142,
        1,0,0,0,30,144,1,0,0,0,32,152,1,0,0,0,34,172,1,0,0,0,36,174,1,0,
        0,0,38,190,1,0,0,0,40,192,1,0,0,0,42,194,1,0,0,0,44,50,3,2,1,0,45,
        50,3,4,2,0,46,50,3,8,4,0,47,50,3,10,5,0,48,50,3,12,6,0,49,44,1,0,
        0,0,49,45,1,0,0,0,49,46,1,0,0,0,49,47,1,0,0,0,49,48,1,0,0,0,50,1,
        1,0,0,0,51,52,5,1,0,0,52,53,5,2,0,0,53,54,3,40,20,0,54,55,5,17,0,
        0,55,56,3,20,10,0,56,57,5,18,0,0,57,3,1,0,0,0,58,59,5,3,0,0,59,60,
        5,4,0,0,60,61,3,40,20,0,61,62,5,17,0,0,62,63,3,16,8,0,63,64,5,18,
        0,0,64,65,5,5,0,0,65,66,3,6,3,0,66,5,1,0,0,0,67,68,5,17,0,0,68,69,
        3,24,12,0,69,77,5,18,0,0,70,71,5,16,0,0,71,72,5,17,0,0,72,73,3,24,
        12,0,73,74,5,18,0,0,74,76,1,0,0,0,75,70,1,0,0,0,76,79,1,0,0,0,77,
        75,1,0,0,0,77,78,1,0,0,0,78,7,1,0,0,0,79,77,1,0,0,0,80,81,5,6,0,
        0,81,82,3,14,7,0,82,83,5,7,0,0,83,86,3,40,20,0,84,85,5,8,0,0,85,
        87,3,28,14,0,86,84,1,0,0,0,86,87,1,0,0,0,87,9,1,0,0,0,88,89,5,9,
        0,0,89,90,3,40,20,0,90,91,5,10,0,0,91,94,3,36,18,0,92,93,5,8,0,0,
        93,95,3,28,14,0,94,92,1,0,0,0,94,95,1,0,0,0,95,11,1,0,0,0,96,97,
        5,11,0,0,97,98,5,7,0,0,98,101,3,40,20,0,99,100,5,8,0,0,100,102,3,
        28,14,0,101,99,1,0,0,0,101,102,1,0,0,0,102,13,1,0,0,0,103,106,5,
        14,0,0,104,106,3,16,8,0,105,103,1,0,0,0,105,104,1,0,0,0,106,15,1,
        0,0,0,107,112,3,40,20,0,108,109,5,16,0,0,109,111,3,40,20,0,110,108,
        1,0,0,0,111,114,1,0,0,0,112,110,1,0,0,0,112,113,1,0,0,0,113,17,1,
        0,0,0,114,112,1,0,0,0,115,116,3,40,20,0,116,117,3,22,11,0,117,19,
        1,0,0,0,118,123,3,18,9,0,119,120,5,16,0,0,120,122,3,18,9,0,121,119,
        1,0,0,0,122,125,1,0,0,0,123,121,1,0,0,0,123,124,1,0,0,0,124,21,1,
        0,0,0,125,123,1,0,0,0,126,127,7,0,0,0,127,23,1,0,0,0,128,133,3,26,
        13,0,129,130,5,16,0,0,130,132,3,26,13,0,131,129,1,0,0,0,132,135,
        1,0,0,0,133,131,1,0,0,0,133,134,1,0,0,0,134,25,1,0,0,0,135,133,1,
        0,0,0,136,141,5,24,0,0,137,141,5,22,0,0,138,141,5,23,0,0,139,141,
        3,42,21,0,140,136,1,0,0,0,140,137,1,0,0,0,140,138,1,0,0,0,140,139,
        1,0,0,0,141,27,1,0,0,0,142,143,3,30,15,0,143,29,1,0,0,0,144,149,
        3,32,16,0,145,146,5,13,0,0,146,148,3,32,16,0,147,145,1,0,0,0,148,
        151,1,0,0,0,149,147,1,0,0,0,149,150,1,0,0,0,150,31,1,0,0,0,151,149,
        1,0,0,0,152,157,3,34,17,0,153,154,5,12,0,0,154,156,3,34,17,0,155,
        153,1,0,0,0,156,159,1,0,0,0,157,155,1,0,0,0,157,158,1,0,0,0,158,
        33,1,0,0,0,159,157,1,0,0,0,160,161,5,17,0,0,161,162,3,28,14,0,162,
        163,5,18,0,0,163,173,1,0,0,0,164,165,3,40,20,0,165,166,5,15,0,0,
        166,167,3,26,13,0,167,173,1,0,0,0,168,169,3,40,20,0,169,170,5,15,
        0,0,170,171,3,40,20,0,171,173,1,0,0,0,172,160,1,0,0,0,172,164,1,
        0,0,0,172,168,1,0,0,0,173,35,1,0,0,0,174,179,3,38,19,0,175,176,5,
        16,0,0,176,178,3,38,19,0,177,175,1,0,0,0,178,181,1,0,0,0,179,177,
        1,0,0,0,179,180,1,0,0,0,180,37,1,0,0,0,181,179,1,0,0,0,182,183,3,
        40,20,0,183,184,5,15,0,0,184,185,3,26,13,0,185,191,1,0,0,0,186,187,
        3,40,20,0,187,188,5,15,0,0,188,189,3,40,20,0,189,191,1,0,0,0,190,
        182,1,0,0,0,190,186,1,0,0,0,191,39,1,0,0,0,192,193,5,25,0,0,193,
        41,1,0,0,0,194,195,5,26,0,0,195,43,1,0,0,0,15,49,77,86,94,101,105,
        112,123,133,140,149,157,172,179,190
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
    RULE_valueTupleList = 3
    RULE_selectStmt = 4
    RULE_updateStmt = 5
    RULE_deleteStmt = 6
    RULE_selectColumns = 7
    RULE_columnList = 8
    RULE_columnDef = 9
    RULE_columnDefList = 10
    RULE_typeName = 11
    RULE_valueList = 12
    RULE_valueLit = 13
    RULE_whereExpr = 14
    RULE_whereOr = 15
    RULE_whereAnd = 16
    RULE_whereAtom = 17
    RULE_assignmentList = 18
    RULE_assignment = 19
    RULE_identifier = 20
    RULE_stringLiteral = 21

    ruleNames =  [ "statement", "createTable", "insertInto", "valueTupleList", 
                   "selectStmt", "updateStmt", "deleteStmt", "selectColumns", 
                   "columnList", "columnDef", "columnDefList", "typeName", 
                   "valueList", "valueLit", "whereExpr", "whereOr", "whereAnd", 
                   "whereAtom", "assignmentList", "assignment", "identifier", 
                   "stringLiteral" ]

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
            self.state = 49
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [1]:
                self.enterOuterAlt(localctx, 1)
                self.state = 44
                self.createTable()
                pass
            elif token in [3]:
                self.enterOuterAlt(localctx, 2)
                self.state = 45
                self.insertInto()
                pass
            elif token in [6]:
                self.enterOuterAlt(localctx, 3)
                self.state = 46
                self.selectStmt()
                pass
            elif token in [9]:
                self.enterOuterAlt(localctx, 4)
                self.state = 47
                self.updateStmt()
                pass
            elif token in [11]:
                self.enterOuterAlt(localctx, 5)
                self.state = 48
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
            self.state = 51
            self.match(SimpleSQLParser.CREATE)
            self.state = 52
            self.match(SimpleSQLParser.TABLE)
            self.state = 53
            self.identifier()
            self.state = 54
            self.match(SimpleSQLParser.LPAREN)
            self.state = 55
            self.columnDefList()
            self.state = 56
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


        def LPAREN(self):
            return self.getToken(SimpleSQLParser.LPAREN, 0)

        def columnList(self):
            return self.getTypedRuleContext(SimpleSQLParser.ColumnListContext,0)


        def RPAREN(self):
            return self.getToken(SimpleSQLParser.RPAREN, 0)

        def VALUES(self):
            return self.getToken(SimpleSQLParser.VALUES, 0)

        def valueTupleList(self):
            return self.getTypedRuleContext(SimpleSQLParser.ValueTupleListContext,0)


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
            self.state = 58
            self.match(SimpleSQLParser.INSERT)
            self.state = 59
            self.match(SimpleSQLParser.INTO)
            self.state = 60
            self.identifier()
            self.state = 61
            self.match(SimpleSQLParser.LPAREN)
            self.state = 62
            self.columnList()
            self.state = 63
            self.match(SimpleSQLParser.RPAREN)
            self.state = 64
            self.match(SimpleSQLParser.VALUES)
            self.state = 65
            self.valueTupleList()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ValueTupleListContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def LPAREN(self, i:int=None):
            if i is None:
                return self.getTokens(SimpleSQLParser.LPAREN)
            else:
                return self.getToken(SimpleSQLParser.LPAREN, i)

        def valueList(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(SimpleSQLParser.ValueListContext)
            else:
                return self.getTypedRuleContext(SimpleSQLParser.ValueListContext,i)


        def RPAREN(self, i:int=None):
            if i is None:
                return self.getTokens(SimpleSQLParser.RPAREN)
            else:
                return self.getToken(SimpleSQLParser.RPAREN, i)

        def COMMA(self, i:int=None):
            if i is None:
                return self.getTokens(SimpleSQLParser.COMMA)
            else:
                return self.getToken(SimpleSQLParser.COMMA, i)

        def getRuleIndex(self):
            return SimpleSQLParser.RULE_valueTupleList

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitValueTupleList" ):
                return visitor.visitValueTupleList(self)
            else:
                return visitor.visitChildren(self)




    def valueTupleList(self):

        localctx = SimpleSQLParser.ValueTupleListContext(self, self._ctx, self.state)
        self.enterRule(localctx, 6, self.RULE_valueTupleList)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 67
            self.match(SimpleSQLParser.LPAREN)
            self.state = 68
            self.valueList()
            self.state = 69
            self.match(SimpleSQLParser.RPAREN)
            self.state = 77
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==16:
                self.state = 70
                self.match(SimpleSQLParser.COMMA)
                self.state = 71
                self.match(SimpleSQLParser.LPAREN)
                self.state = 72
                self.valueList()
                self.state = 73
                self.match(SimpleSQLParser.RPAREN)
                self.state = 79
                self._errHandler.sync(self)
                _la = self._input.LA(1)

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
        self.enterRule(localctx, 8, self.RULE_selectStmt)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 80
            self.match(SimpleSQLParser.SELECT)
            self.state = 81
            self.selectColumns()
            self.state = 82
            self.match(SimpleSQLParser.FROM)
            self.state = 83
            self.identifier()
            self.state = 86
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==8:
                self.state = 84
                self.match(SimpleSQLParser.WHERE)
                self.state = 85
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
        self.enterRule(localctx, 10, self.RULE_updateStmt)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 88
            self.match(SimpleSQLParser.UPDATE)
            self.state = 89
            self.identifier()
            self.state = 90
            self.match(SimpleSQLParser.SET)
            self.state = 91
            self.assignmentList()
            self.state = 94
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==8:
                self.state = 92
                self.match(SimpleSQLParser.WHERE)
                self.state = 93
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
        self.enterRule(localctx, 12, self.RULE_deleteStmt)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 96
            self.match(SimpleSQLParser.DELETE)
            self.state = 97
            self.match(SimpleSQLParser.FROM)
            self.state = 98
            self.identifier()
            self.state = 101
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==8:
                self.state = 99
                self.match(SimpleSQLParser.WHERE)
                self.state = 100
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
        self.enterRule(localctx, 14, self.RULE_selectColumns)
        try:
            self.state = 105
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [14]:
                self.enterOuterAlt(localctx, 1)
                self.state = 103
                self.match(SimpleSQLParser.STAR)
                pass
            elif token in [25]:
                self.enterOuterAlt(localctx, 2)
                self.state = 104
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
        self.enterRule(localctx, 16, self.RULE_columnList)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 107
            self.identifier()
            self.state = 112
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==16:
                self.state = 108
                self.match(SimpleSQLParser.COMMA)
                self.state = 109
                self.identifier()
                self.state = 114
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
        self.enterRule(localctx, 18, self.RULE_columnDef)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 115
            self.identifier()
            self.state = 116
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
        self.enterRule(localctx, 20, self.RULE_columnDefList)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 118
            self.columnDef()
            self.state = 123
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==16:
                self.state = 119
                self.match(SimpleSQLParser.COMMA)
                self.state = 120
                self.columnDef()
                self.state = 125
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
        self.enterRule(localctx, 22, self.RULE_typeName)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 126
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
        self.enterRule(localctx, 24, self.RULE_valueList)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 128
            self.valueLit()
            self.state = 133
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==16:
                self.state = 129
                self.match(SimpleSQLParser.COMMA)
                self.state = 130
                self.valueLit()
                self.state = 135
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
        self.enterRule(localctx, 26, self.RULE_valueLit)
        try:
            self.state = 140
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [24]:
                self.enterOuterAlt(localctx, 1)
                self.state = 136
                self.match(SimpleSQLParser.INTEGER_LITERAL)
                pass
            elif token in [22]:
                self.enterOuterAlt(localctx, 2)
                self.state = 137
                self.match(SimpleSQLParser.TRUE)
                pass
            elif token in [23]:
                self.enterOuterAlt(localctx, 3)
                self.state = 138
                self.match(SimpleSQLParser.FALSE)
                pass
            elif token in [26]:
                self.enterOuterAlt(localctx, 4)
                self.state = 139
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
        self.enterRule(localctx, 28, self.RULE_whereExpr)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 142
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
        self.enterRule(localctx, 30, self.RULE_whereOr)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 144
            self.whereAnd()
            self.state = 149
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==13:
                self.state = 145
                self.match(SimpleSQLParser.OR)
                self.state = 146
                self.whereAnd()
                self.state = 151
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
        self.enterRule(localctx, 32, self.RULE_whereAnd)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 152
            self.whereAtom()
            self.state = 157
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==12:
                self.state = 153
                self.match(SimpleSQLParser.AND)
                self.state = 154
                self.whereAtom()
                self.state = 159
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
        self.enterRule(localctx, 34, self.RULE_whereAtom)
        try:
            self.state = 172
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,12,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 160
                self.match(SimpleSQLParser.LPAREN)
                self.state = 161
                self.whereExpr()
                self.state = 162
                self.match(SimpleSQLParser.RPAREN)
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 164
                self.identifier()
                self.state = 165
                self.match(SimpleSQLParser.EQ)
                self.state = 166
                self.valueLit()
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 168
                self.identifier()
                self.state = 169
                self.match(SimpleSQLParser.EQ)
                self.state = 170
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
        self.enterRule(localctx, 36, self.RULE_assignmentList)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 174
            self.assignment()
            self.state = 179
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==16:
                self.state = 175
                self.match(SimpleSQLParser.COMMA)
                self.state = 176
                self.assignment()
                self.state = 181
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
        self.enterRule(localctx, 38, self.RULE_assignment)
        try:
            self.state = 190
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,14,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 182
                self.identifier()
                self.state = 183
                self.match(SimpleSQLParser.EQ)
                self.state = 184
                self.valueLit()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 186
                self.identifier()
                self.state = 187
                self.match(SimpleSQLParser.EQ)
                self.state = 188
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
        self.enterRule(localctx, 40, self.RULE_identifier)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 192
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
        self.enterRule(localctx, 42, self.RULE_stringLiteral)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 194
            self.match(SimpleSQLParser.STRING_LITERAL)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx





