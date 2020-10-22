%{
  #include <stdio.h>
  #include <string.h>
  extern void yyerror();
  extern int yylex();
  extern char* yytext;
  extern int yylineno;
%}


%define parse.lac full
%define parse.error verbose

%union{
	char* dataType;
	char charVal;
	int intVal;
	float floatVal;
	char* strVal;
}


%token EQUAL
%token SEMICOLON
%token COMMA
%token OPEN_P
%token CLOSE_P
%token REMAINING
%token NOT
%token MINUS
%token PLUS
%token MULT
%token GREATER
%token LESS
%token DIV_INT
%token DIV
%token OPEN_CB
%token CLOSE_CB
%token INT
%token CHAR
%token FLOAT
%token BOOL
%token LAMBDA
%token VOID

%token	INC_OP DEC_OP LE_OP GE_OP EQ_OP NE_OP
%token	AND_OP OR_OP
%token	IF ELIF ELSE WHILE END
%token	PRINT
%token TRUE FALSE //bool


%token <charVal> CHARACTER_VALUE
%token <intVal> INTEGER_VALUE
%token <floatVal> FLOAT_VALUE
%token <strVal> STRING_VALUE
%token <strVal> IDENTIFIER_VALUE


/* Nao terminais */
%type <strVal> _FUNC_DEF
%type <strVal> _WHILE
%type <strVal> _IF
%type <strVal> _ELIF
%type <strVal> _CONDITION
%type <strVal> STMT
%type <strVal> ARGS_N
%type <strVal> ARGS2_N
%type <strVal> _CONDITION_OP
%type <strVal> _EXPR
%type <strVal> _TERM
%type <strVal> _FACTOR
%type <strVal> _REL_EXPR
%type <strVal> DATA_TYPE


%% 
PROGRAM: OPEN_CB BLOCK CLOSE_CB;

BLOCK: STMT
      | STMT BLOCK
;

STMT: _FUNC_DEF
			| _WHILE
			| _IF
			| DATA_TYPE IDENTIFIER_VALUE EQUAL _CONDITION SEMICOLON
			| PRINT OPEN_P _CONDITION CLOSE_P SEMICOLON
;
DATA_TYPE: INT
      | BOOL
			| CHAR
			| FLOAT
      | VOID
;
_FUNC_DEF: DATA_TYPE IDENTIFIER_VALUE OPEN_P ARGS_N CLOSE_P OPEN_CB BLOCK CLOSE_CB  SEMICOLON
          | LAMBDA OPEN_P ARGS_N CLOSE_P OPEN_CB BLOCK CLOSE_CB  SEMICOLON;

_WHILE: WHILE OPEN_P _CONDITION CLOSE_P OPEN_CB BLOCK CLOSE_CB  SEMICOLON;

_IF: IF OPEN_P _CONDITION CLOSE_P OPEN_CB BLOCK CLOSE_CB  END SEMICOLON
	| IF OPEN_P _CONDITION CLOSE_P OPEN_CB BLOCK CLOSE_CB  _ELIF END SEMICOLON
;

_ELIF: ELSE OPEN_CB BLOCK CLOSE_CB 
		| ELIF OPEN_P _CONDITION CLOSE_P OPEN_CB BLOCK CLOSE_CB  ELSE OPEN_CB BLOCK CLOSE_CB 
;
FUNC_IDENTIFIER_VALUE: IDENTIFIER_VALUE OPEN_P ARGS2_N CLOSE_P;
_CONDITION: _REL_EXPR
			| _REL_EXPR AND_OP _CONDITION
			| _REL_EXPR OR_OP _CONDITION
;

_REL_EXPR: _EXPR
		| _EXPR _CONDITION_OP _REL_EXPR
;

_EXPR: _TERM
		| _TERM PLUS _EXPR
		| _TERM MINUS _EXPR
;

_TERM: _FACTOR
		| _FACTOR MULT _TERM
		| _FACTOR DIV _TERM
		| _FACTOR REMAINING _TERM
;

_FACTOR: INTEGER_VALUE
			| FLOAT_VALUE
			| TRUE
			| FALSE
			| STRING_VALUE
			| CHARACTER_VALUE
			| PLUS _FACTOR
			| MINUS _FACTOR
      | NOT _FACTOR
			| OPEN_P _CONDITION CLOSE_P
			| IDENTIFIER_VALUE
			| FUNC_IDENTIFIER_VALUE
;

_CONDITION_OP: EQ_OP
			| GREATER 
			| GE_OP 
			| LESS 
			| LE_OP
;

ARGS_N: DATA_TYPE IDENTIFIER_VALUE 
    | DATA_TYPE IDENTIFIER_VALUE COMMA ARGS_N
;

ARGS2_N: _CONDITION
		| DATA_TYPE IDENTIFIER_VALUE
		| _CONDITION COMMA ARGS2_N
		| DATA_TYPE IDENTIFIER_VALUE COMMA ARGS2_N
;
%%


int main(){

  yyparse();
  printf("No Errors!!\n");
  return 0;
}