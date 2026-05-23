grammar SimpleSQL;

statement
    : createTable
    | insertInto
    | selectStmt
    | updateStmt
    | deleteStmt
    ;

createTable
    : CREATE TABLE identifier LPAREN columnList RPAREN
    ;

insertInto
    : INSERT INTO identifier LPAREN columnList RPAREN VALUES LPAREN valueList RPAREN
    ;

selectStmt
    : SELECT selectColumns FROM identifier (WHERE whereExpr)?
    ;

updateStmt
    : UPDATE identifier SET assignmentList (WHERE whereExpr)?
    ;

deleteStmt
    : DELETE FROM identifier (WHERE whereExpr)?
    ;

selectColumns
    : STAR
    | columnList
    ;

columnList
    : identifier (COMMA identifier)*
    ;

valueList
    : stringLiteral (COMMA stringLiteral)*
    ;

whereExpr
    : whereOr
    ;

whereOr
    : whereAnd (OR whereAnd)*
    ;

whereAnd
    : whereAtom (AND whereAtom)*
    ;

whereAtom
    : LPAREN whereExpr RPAREN
    | identifier EQ stringLiteral
    | identifier EQ identifier
    ;

assignmentList
    : assignment (COMMA assignment)*
    ;

assignment
    : identifier EQ stringLiteral
    | identifier EQ identifier
    ;

identifier
    : IDENTIFIER
    ;

stringLiteral
    : STRING_LITERAL
    ;

CREATE:     'CREATE';
TABLE:      'TABLE';
INSERT:     'INSERT';
INTO:       'INTO';
VALUES:     'VALUES';
SELECT:     'SELECT';
FROM:       'FROM';
WHERE:      'WHERE';
UPDATE:     'UPDATE';
SET:        'SET';
DELETE:     'DELETE';
AND:        'AND';
OR:         'OR';
STAR:       '*';
EQ:         '=';
COMMA:      ',';
LPAREN:     '(';
RPAREN:     ')';

IDENTIFIER: [a-zA-Z_][a-zA-Z0-9_]*;
STRING_LITERAL: '\'' (~['\r\n] | '\'\'')* '\'';

WS: [ \t\r\n]+ -> skip;