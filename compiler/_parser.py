from tokenizer import Tokenizer
from preprocessor import PrePro
from node import *


class Parser:
    tokens = None

    @staticmethod
    def run(code):
        processed_code = PrePro.filter(code)
        Parser.tokens = Tokenizer(processed_code)
        Parser.tokens.selectNext()
        res = Parser.parseProgram()
        if Parser.tokens.actual._type == "EOF":
            return res
        else:
            raise SyntaxError(
                f"TOKEN INVALIDO: esperado token do tipo {'EOF'}, recebido {Parser.tokens.actual.value} na posicao: ({Parser.tokens.position})")

    @staticmethod
    def parseExpression():
        res = Parser.parseTerm()
        while (Parser.tokens.actual._type == 'PLUS' or Parser.tokens.actual._type == 'MINUS' or Parser.tokens.actual._type == "OR_OP"):
            if Parser.tokens.actual._type == 'PLUS' or Parser.tokens.actual._type == 'MINUS' or Parser.tokens.actual._type == "OR_OP":
                res = BinOP(Parser.tokens.actual.value,
                            [res, None])
                Parser.tokens.selectNext()
                res.children[1] = Parser.parseTerm()

            else:
                raise SyntaxError(
                    f"TOKEN INVALIDO: token desconhecido encontrado: {Parser.tokens.actual.value} na posicao: ({Parser.tokens.position})")
        return res

    @staticmethod
    def parseRelExpression():
        res = Parser.parseExpression()
        while (Parser.tokens.actual._type == 'EQ_OP' or Parser.tokens.actual._type == 'G0_OP' or Parser.tokens.actual._type == 'L0_OP'):
            if Parser.tokens.actual._type == 'EQ_OP' or Parser.tokens.actual._type == 'G0_OP' or Parser.tokens.actual._type == 'L0_OP':
                res = BinOP(Parser.tokens.actual.value,
                            [res, None])
                Parser.tokens.selectNext()
                res.children[1] = Parser.parseTerm()

            else:
                raise SyntaxError(
                    f"TOKEN INVALIDO: token desconhecido encontrado: {Parser.tokens.actual.value} na posicao: ({Parser.tokens.position})")
        return res

    @staticmethod
    def parseTerm():
        res = Parser.parseFactor()
        while (Parser.tokens.actual._type == 'DIV' or Parser.tokens.actual._type == 'MULT' or Parser.tokens.actual._type == 'AND_OP'):
            if Parser.tokens.actual._type == 'DIV' or Parser.tokens.actual._type == 'MULT' or Parser.tokens.actual._type == 'AND_OP':
                res = BinOP(Parser.tokens.actual.value,
                            [res, None])

                Parser.tokens.selectNext()
                res.children[1] = Parser.parseFactor()

            else:
                raise SyntaxError(
                    f"TOKEN INVALIDO: token desconhecido encontrado: {Parser.tokens.actual.value} na posicao: ({Parser.tokens.position})")
        return res

    @staticmethod
    def parseFactor():
        if Parser.tokens.actual._type == 'INT':
            res = IntVal(Parser.tokens.actual.value)
            Parser.tokens.selectNext()

        elif Parser.tokens.actual._type == 'BOOL':
            if Parser.tokens.actual.value == "true":
                res = BoolVal(True)
            elif Parser.tokens.actual.value == "false":
                res = BoolVal(False)
            Parser.tokens.selectNext()

        elif Parser.tokens.actual._type == 'STRING':
            res = StringVal(Parser.tokens.actual.value)
            Parser.tokens.selectNext()

        elif Parser.tokens.actual._type == 'PLUS' or Parser.tokens.actual._type == 'MINUS' or Parser.tokens.actual._type == 'NOT_OP':
            res = UnOp(Parser.tokens.actual.value, [None])
            Parser.tokens.selectNext()
            res.children[0] = Parser.parseFactor()

        elif Parser.tokens.actual._type == "OPEN_PARENTHESIS":
            Parser.tokens.selectNext()
            res = Parser.parseRelExpression()

            if Parser.tokens.actual._type == "CLOSED_PARENTHESIS":
                Parser.tokens.selectNext()
            else:
                raise SyntaxError(
                    f'SINTAXE INVALIDA: faltando "CLOSED_PARENTHESIS"({Parser.tokens.actual.value}) na posicao: ({Parser.tokens.position}, parenteses são abertos mas nunca fechados)')
        elif Parser.tokens.actual._type == "IDENTIFIER":
            ident_value = Parser.tokens.actual.value
            Parser.tokens.selectNext()
            if(Parser.tokens.actual._type == 'OPEN_PARENTHESIS'):
                res = FuncCall(ident_value)
                Parser.tokens.selectNext()
                if(Parser.tokens.actual._type != 'CLOSED_PARENTHESIS'):
                    res.children.append(Parser.parseRelExpression())
                    while(Parser.tokens.actual._type == 'COMMA'):
                        Parser.tokens.selectNext()
                        res.children.append(Parser.parseRelExpression())
                if(Parser.tokens.actual._type == 'CLOSED_PARENTHESIS'):
                    Parser.tokens.selectNext()
                else:
                    raise SyntaxError(
                        f'SINTAXE INVALIDA: faltando "CLOSED_PARENTHESIS"({Parser.tokens.actual.value}) na posicao: ({Parser.tokens.position}, parenteses são abertos mas nunca fechados)')
            else:
                res = Identifier(ident_value)
            return res

        else:
            raise SyntaxError(
                f"TOKEN INVALIDO: token esperado ' (INT) or (PLUS) or (MINUS) or (OPEN_PARENTHESIS) or (CLOSED_PARENTHESIS) ', recebido -{Parser.tokens.actual.value} na posicao: ({Parser.tokens.position})")
        return res

    @staticmethod
    def parseBlock():
        stmt = Statement([])
        while (Parser.tokens.actual._type != 'EOF' and Parser.tokens.actual._type != 'END' and Parser.tokens.actual._type != 'ELSEIF' and Parser.tokens.actual._type != 'ELSE'):
            stmt.children.append(Parser.parseCommand())

        return stmt

    @staticmethod
    def parseCommand():
        res = None
        if Parser.tokens.actual._type == "TYPE":
            _type = VarType(Parser.tokens.actual.value)
            Parser.tokens.selectNext()
            if Parser.tokens.actual._type == "IDENTIFIER":
                res = Identifier(Parser.tokens.actual.value)
                res = VarDec(None, [res, _type])

                Parser.tokens.selectNext()
            else:
                SyntaxError(
                    f'Sintaxe invalida: esperando token  "IDENTIFIER", recebido ({Parser.tokens.actual.value}) na posicao: ({Parser.tokens.position})')

        elif Parser.tokens.actual._type == "RETURN":
            node = Return()
            Parser.tokens.selectNext()
            node.children.append(Parser.parseRelExpression())
            if Parser.tokens.actual._type == "NEW_LINE":
                Parser.tokens.selectNext()
                return node
            else:
                raise Exception(
                    f"Esperado '\\n', recebido '{Parser.tokens.actual.value}'")

        elif Parser.tokens.actual._type == "IDENTIFIER":
            var = Parser.tokens.actual
            Parser.tokens.selectNext()
            if(Parser.tokens.actual._type == 'OPEN_PARENTHESIS'):
                node = FuncCall(var.value)
                Parser.tokens.selectNext()
                if(Parser.tokens.actual._type != 'CLOSED_PARENTHESIS'):
                    node.children.append(Parser.parseRelExpression())
                    while(Parser.tokens.actual._type == 'COMMA'):
                        Parser.tokens.selectNext()
                        node.children.append(Parser.parseRelExpression())
                if(Parser.tokens.actual._type == 'CLOSED_PARENTHESIS'):
                    Parser.tokens.selectNext()
                    if Parser.tokens.actual._type == "NEW_LINE":
                        Parser.tokens.selectNext()
                        return node
                else:
                    raise SyntaxError(
                        f"ESPERADO CLOSED_PARENTHESIS, instead received {Parser.tokens.actual._type}")

            else:
                if Parser.tokens.actual._type == "EQUAL":
                    res = Assignment(Parser.tokens.actual.value, [
                        var, None])
                    Parser.tokens.selectNext()
                    if Parser.tokens.actual._type == "READLINE":
                        Parser.tokens.selectNext()
                        if Parser.tokens.actual._type == "OPEN_PARENTHESIS":
                            Parser.tokens.selectNext()
                            if Parser.tokens.actual._type == "CLOSED_PARENTHESIS":
                                Parser.tokens.selectNext()
                                res.children[1] = Readline()
                                if Parser.tokens.actual._type == "NEW_LINE":
                                    Parser.tokens.selectNext()
                                else:
                                    raise SyntaxError(
                                        f"Esperado '\\n', recebido '{Parser.tokens.actual.value}'")
                            else:
                                raise SyntaxError(
                                    f'SINTAXE INVALIDA: faltando "CLOSED_PARENTHESIS"({Parser.tokens.actual.value}) na posicao: ({Parser.tokens.position}, parenteses são abertos mas nunca fechados)')

                    else:
                        res.children[1] = Parser.parseRelExpression()
                        if Parser.tokens.actual._type == "NEW_LINE":
                            Parser.tokens.selectNext()
                        else:
                            raise SyntaxError(
                                f"Esperado '\\n', recebido '{Parser.tokens.actual.value}'")
                else:
                    raise SyntaxError(
                        f"Esperado '=', recebido '{Parser.tokens.actual.value}'")
        elif Parser.tokens.actual._type == "PRINT":
            Parser.tokens.selectNext()
            if Parser.tokens.actual._type == "OPEN_PARENTHESIS":
                Parser.tokens.selectNext()
                res = Print(Parser.tokens.actual.value, [
                            Parser.parseRelExpression()])

                if Parser.tokens.actual._type == "CLOSED_PARENTHESIS":
                    Parser.tokens.selectNext()
                    if Parser.tokens.actual._type == "NEW_LINE":
                        Parser.tokens.selectNext()
                    else:
                        raise SyntaxError(
                            f"Esperado '\\n', recebido '{Parser.tokens.actual.value}'")
                else:
                    raise SyntaxError(
                        f'SINTAXE INVALIDA: faltando "CLOSED_PARENTHESIS"({Parser.tokens.actual.value}) na posicao: ({Parser.tokens.position}, parenteses são abertos mas nunca fechados)')
            else:
                raise SyntaxError(
                    f'SINTAXE INVALIDA: faltando "OPEN_PARENTHESIS" depois da chamada mostre, recebido ({Parser.tokens.actual.value}) na posicao: ({Parser.tokens.position})')

        elif Parser.tokens.actual._type == "WHILE":
            Parser.tokens.selectNext()
            res = While(Parser.tokens.actual.value, [
                None, None])
            res.children[0] = Parser.parseRelExpression()
            if Parser.tokens.actual._type == "NEW_LINE":
                Parser.tokens.selectNext()
                res.children[1] = Parser.parseBlock()
                if Parser.tokens.actual._type == "END":
                    Parser.tokens.selectNext()
                    if Parser.tokens.actual._type == "NEW_LINE":
                        Parser.tokens.selectNext()
                    else:
                        raise SyntaxError(
                            f"Esperado '\\n', recebido '{Parser.tokens.actual.value}'")

                else:
                    raise SyntaxError(
                        f'TOKEN INESPERADO: recebido ({Parser.tokens.actual.value}) na posicao: ({Parser.tokens.position}), ESPERADO END depois do enquanto')
            else:
                raise SyntaxError(
                    f"Esperado '\\n', recebido '{Parser.tokens.actual.value}'")

        elif Parser.tokens.actual._type == "IF":
            Parser.tokens.selectNext()
            res = IF(Parser.tokens.actual.value, [
                     Parser.parseRelExpression(), None, None])

            last = None
            current = None

            if Parser.tokens.actual._type == "NEW_LINE":
                Parser.tokens.selectNext()
                res.children[1] = Parser.parseBlock()

                while Parser.tokens.actual._type == "ELSEIF":
                    Parser.tokens.selectNext()

                    current = IF(Parser.tokens.actual.value, [
                                 Parser.parseRelExpression(), None, None])

                    if Parser.tokens.actual._type == "NEW_LINE":
                        Parser.tokens.selectNext()

                        current.children[1] = Parser.parseBlock()

                        if last is None:
                            res.children[2] = current

                        else:
                            last.children[2] = current

                        last = current

                if Parser.tokens.actual._type == "ELSE":
                    Parser.tokens.selectNext()

                    if Parser.tokens.actual._type == "NEW_LINE":
                        Parser.tokens.selectNext()

                        if last is None:
                            res.children[2] = Parser.parseBlock()

                        else:
                            last.children[2] = Parser.parseBlock()

                if Parser.tokens.actual._type == "END":
                    Parser.tokens.selectNext()

                    if Parser.tokens.actual._type == "NEW_LINE":
                        Parser.tokens.selectNext()

        elif Parser.tokens.actual._type == "NEW_LINE":
            Parser.tokens.selectNext()
            if res is None:
                res = NoOP(Parser.tokens.actual.value)
        else:
            raise SyntaxError(
                f'TOKEN INESPERADO: recebido ({Parser.tokens.actual.value}) na posicao: ({Parser.tokens.position})')
        return res

    @staticmethod
    def parseProgram():
        statements = Statement([])
        while(Parser.tokens.actual._type != "EOF"):
            if(Parser.tokens.actual._type == "FUNCTION_DEC"):
                Parser.tokens.selectNext()
                if(Parser.tokens.actual._type == "IDENTIFIER"):
                    funcDec = FuncDec(Parser.tokens.actual.value, [], None)
                    statements.children.append(funcDec)
                    Parser.tokens.selectNext()
                    if(Parser.tokens.actual._type == "OPEN_PARENTHESIS"):
                        Parser.tokens.selectNext()
                        if Parser.tokens.actual._type == "TYPE":
                            _type = Parser.tokens.actual.value
                            Parser.tokens.selectNext()
                            arg = []
                            if Parser.tokens.actual._type == "IDENTIFIER":
                                arg.append(Parser.tokens.actual.value)
                                arg.append(_type)
                                funcDec.children.append(arg)
                                Parser.tokens.selectNext()
                                while(Parser.tokens.actual._type == "COMMA"):
                                    Parser.tokens.selectNext()
                                    if(Parser.tokens.actual._type == "TYPE"):
                                        arg = []
                                        arg.append(
                                            Parser.tokens.actual.value)
                                        Parser.tokens.selectNext()
                                        if(Parser.tokens.actual._type == "IDENTIFIER"):
                                            arg.append(
                                                Parser.tokens.actual.value)

                                            funcDec.children.append(
                                                arg)
                                            Parser.tokens.selectNext()
                                        else:
                                            raise SyntaxError(
                                                f'TOKEN INESPERADO: recebido ({Parser.tokens.actual.value}) na posicao: ({Parser.tokens.position}), esperando IDENTIFIER ')
                                    else:
                                        raise SyntaxError(
                                            f'TOKEN INESPERADO: recebido ({Parser.tokens.actual.value}) na posicao: ({Parser.tokens.position}), esperando TYPE')

                        if(Parser.tokens.actual._type == "CLOSED_PARENTHESIS"):
                            Parser.tokens.selectNext()
                            if Parser.tokens.actual._type == "RET_TYPE":
                                Parser.tokens.selectNext()
                                if(Parser.tokens.actual._type == "TYPE"):
                                    funcDec.type = Parser.tokens.actual.value
                                    Parser.tokens.selectNext()
                                    if(Parser.tokens.actual._type == "NEW_LINE"):
                                        Parser.tokens.selectNext()
                                        funcBlock = Parser.parseBlock()
                                        funcDec.children.append(funcBlock)
                                        if(Parser.tokens.actual._type == "END"):
                                            Parser.tokens.selectNext()
                                            if(Parser.tokens.actual._type == "NEW_LINE"):
                                                Parser.tokens.selectNext()
                                            else:
                                                raise SyntaxError(
                                                    f"Esperado '\\n', recebido '{Parser.tokens.actual.value}'")
                                        else:
                                            SyntaxError(
                                                f'TOKEN INESPERADO: recebido ({Parser.tokens.actual.value}) na posicao: ({Parser.tokens.position}), esperando END')
                                    else:
                                        raise SyntaxError(
                                            f"Esperado '\\n', recebido '{Parser.tokens.actual.value}'")
                                else:
                                    raise SyntaxError(
                                        f'TOKEN INESPERADO: recebido ({Parser.tokens.actual.value}) na posicao: ({Parser.tokens.position}), esperando TYPE ')
                        else:
                            raise SyntaxError(
                                f'TOKEN INESPERADO: recebido ({Parser.tokens.actual.value}) na posicao: ({Parser.tokens.position}), esperando CLOSED_PARENTHESIS ')
                    else:
                        raise SyntaxError(
                            f'TOKEN INESPERADO: recebido ({Parser.tokens.actual.value}) na posicao: ({Parser.tokens.position}), esperando OPEN_PARENTHESIS ')
                else:
                    raise SyntaxError(
                        f'TOKEN INESPERADO: recebido ({Parser.tokens.actual.value}) na posicao: ({Parser.tokens.position}), esperando IDENTIFIER ')
            else:
                statements.children.append(Parser.parseCommand())
        return statements
