%{
    #include <string.h>
    #include <stdlib.h>
    #include "y.tab.h"
    void extern yyerror(char*);
    void InvalidToken();

%}

whitespace      [ \t\r\v\f]
linefeed        \n

%%
";"					    { return SEMICOLON; }
","					    { return COMMA; }
"="				        { return EQUAL; }
"("					    { return OPEN_P; }
")"					    { return CLOSE_P; }
"%"						{ return REMAINING; }
"-"					    { return MINUS; }
"+"					    { return PLUS; }
"*"					    { return MULT; }
"<"					    { return LESS; }
">"					    { return GREATER; }
"//"					{return DIV_INT;}
"/"						{return DIV;}
"{"					    { return OPEN_CB; }
"}"					    { return CLOSE_CB; }
"true"                  { return TRUE; }
"false"                 { return FALSE; }
"!"                     { return NOT; }
"++"					{ return INC_OP; }
"--"					{ return DEC_OP; }
"&&"					{ return AND_OP; }
"||"					{ return OR_OP; }
"<="					{ return LE_OP; }
">="					{ return GE_OP; }
"=="					{ return EQ_OP; }
"!="					{ return NE_OP; }
"if"					{ return IF; }
"end"                   { return END; }
"else"					{ return ELSE; }
"elif"					{ return ELIF; }
"while"					{ return WHILE; }
"print"					{ return PRINT; }
"int"					{ return INT; }
"char"					{ return CHAR; }
"float"					{ return FLOAT; }
"bool"					{ return BOOL; }
"void"					{ return VOID; }
"|>"					{ return LAMBDA; }



[\"][a-zA-Z][\"]								{yylval.charVal = yytext[1]; return CHARACTER_VALUE;}
[-+]?[0-9]+                                     {yylval.intVal = atoi(yytext); return INTEGER_VALUE;}
[-+]?[0-9]*\.?[0-9]+                            {yylval.floatVal = atof(yytext); return FLOAT_VALUE;}
[a-zA-Z][_a-zA-Z0-9]*							{yylval.strVal = strdup(yytext); return IDENTIFIER_VALUE;}
\"(\\.|[^"])*\"                                 {yylval.strVal = strdup(yytext); return STRING_VALUE;}



{linefeed}                                      {yylineno++;}
{whitespace}                                    ;
.                                               {InvalidToken();}


%%

int yywrap(void){
    return 1;
}

void yyerror(char *s) {
    fprintf(stderr, "\nERROR ON LINE %d : \n %s\n", yylineno, s);
    exit(0);
}

void InvalidToken(){
    printf("ERROR ON LINE %d : \n Invalid Token %s\n", yylineno,yytext);
    exit(0);
}
