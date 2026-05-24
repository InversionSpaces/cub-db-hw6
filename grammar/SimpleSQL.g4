grammar SimpleSQL;

statement
    : createTable
    | insertInto
    | selectStmt
    | updateStmt
    | deleteStmt
    ;

createTable
    : CREATE TABLE identifier LPAREN columnDefList RPAREN
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

columnDef
    : identifier typeName
    ;

columnDefList
    : columnDef (COMMA columnDef)*
    ;

typeName
    : INT_T
    | BOOL_T
    | TEXT_T
    ;

valueList
    : valueLit (COMMA valueLit)*
    ;

valueLit
    : INTEGER_LITERAL
    | TRUE
    | FALSE
    | stringLiteral
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
    | identifier EQ valueLit
    | identifier EQ identifier
    ;

assignmentList
    : assignment (COMMA assignment)*
    ;

assignment
    : identifier EQ valueLit
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

INT_T:      'INT';
BOOL_T:     'BOOL';
TEXT_T:     'TEXT';
TRUE:       'TRUE';
FALSE:      'FALSE';

INTEGER_LITERAL: '-'? [0-9]+ ;

IDENTIFIER: [a-zA-Z_][a-zA-Z0-9_]*;
STRING_LITERAL: '\'' (~['\r\n] | '\'\'')* '\'';

WS: [ \t\r\n]+ -> skip;
