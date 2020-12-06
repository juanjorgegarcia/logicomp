from typing import List
from symbol_table import *


class Node:
    def __init__(self, value: str, children):
        self.value = value
        self.children = children

    def Evaluate(self, symbolTable):
        pass


class BinOP(Node):
    def __init__(self, value: str, children=[None, None]):
        if children and len(children) == 2:
            super().__init__(value, children)
        else:
            raise SyntaxError(
                f"INVALID OPERATION: BinOP must have 2 children ")

    def Evaluate(self, symbolTable):

        if self.value == "+":
            t1, v1 = self.children[0].Evaluate(symbolTable)
            t2, v2 = self.children[1].Evaluate(symbolTable)

            if(t1 == "str") or (t2 == "str"):
                raise SyntaxError(
                    f"INVALID OPERATION: can't do arithmetics operation on strings")
            return SymbolValue("int", v1 + v2)

        elif self.value == "-":
            t1, v1 = self.children[0].Evaluate(symbolTable)
            t2, v2 = self.children[1].Evaluate(symbolTable)

            if(t1 == "str") or (t2 == "str"):
                raise SyntaxError(
                    f"INVALID OPERATION: can't do arithmetics operation on strings")
            return SymbolValue("int", int(v1 - v2))

        elif self.value == "*":
            t1, v1 = self.children[0].Evaluate(symbolTable)
            t2, v2 = self.children[1].Evaluate(symbolTable)

            if(t1 == "str") or (t2 == "str"):
                v1, v2 = str(v1), str(v2)
                return SymbolValue("str", v1 + v2)

            return SymbolValue("int", int(v1 * v2))

        elif self.value == "/":
            t1, v1 = self.children[0].Evaluate(symbolTable)
            t2, v2 = self.children[1].Evaluate(symbolTable)

            if(t1 == "str") or (t2 == "str"):
                raise SyntaxError(
                    f"INVALID OPERATION: can't do arithmetics operation on strings")
            return SymbolValue("int", int(v1 / v2))

        elif self.value == "==":
            return SymbolValue("bool", bool(self.children[0].Evaluate(symbolTable).value == self.children[1].Evaluate(symbolTable).value))

        elif self.value == ">":
            return SymbolValue("bool", bool(self.children[0].Evaluate(symbolTable).value > self.children[1].Evaluate(symbolTable).value))

        elif self.value == "<":
            return SymbolValue("bool", bool(self.children[0].Evaluate(symbolTable).value < self.children[1].Evaluate(symbolTable).value))

        elif self.value == "&&":
            t1, v1 = self.children[0].Evaluate(symbolTable)
            t2, v2 = self.children[1].Evaluate(symbolTable)

            if(t1 == "str") or (t2 == "str"):
                raise SyntaxError(
                    f"INVALID OPERATION: can't do boolean operation on strings")
            return SymbolValue("bool", bool(v1 and v2))

        elif self.value == "||":
            t1, v1 = self.children[0].Evaluate(symbolTable)
            t2, v2 = self.children[1].Evaluate(symbolTable)

            if(t1 == "str") or (t2 == "str"):
                raise SyntaxError(
                    f"INVALID OPERATION: can't do boolean operation on strings")
            return SymbolValue("bool", bool(v1 or v2))


class UnOp(Node):
    def __init__(self, value: str, children=[None]):
        if children and len(children) == 1:
            super().__init__(value, children)
        else:
            raise SyntaxError(
                f"INVALID OPERATION: UnOp must have 1 children ")

    def Evaluate(self, symbolTable):
        if self.value == "+":
            return SymbolValue("int", self.children[0].Evaluate(symbolTable).value)
        if self.value == "-":
            return SymbolValue("int", -self.children[0].Evaluate(symbolTable).value)
        if self.value == "!":
            return SymbolValue("bool", not(self.children[0].Evaluate(symbolTable).value))


class IntVal(Node):
    def __init__(self, value: str):
        super().__init__(int(value), None)

    def Evaluate(self, symbolTable):
        return SymbolValue("int", self.value)


class NoOP(Node):
    def __init__(self, value: str):
        super().__init__(value, None)

    def Evaluate(self, symbolTable):
        pass


class Assignment(Node):
    def __init__(self, value: str, children):
        if children and len(children) == 2:
            super().__init__(value, children)
        else:
            raise SyntaxError(
                f"INVALID OPERATION: Assigment must have 2 children ")

    def Evaluate(self, symbolTable):
        symbolTable.set_symbol(
            self.children[0].value, self.children[1].Evaluate(symbolTable))


class Identifier(Node):
    def __init__(self, value: str):
        super().__init__(value, [])

    def Evaluate(self, symbolTable):
        return symbolTable.get(self.value)


class Print(Node):
    def __init__(self, value: str, children=[None]):
        if children and len(children) == 1:
            super().__init__(value, children)
        else:
            raise SyntaxError(
                f"INVALID OPERATION: Print must have 1 child ")

    def Evaluate(self, symbolTable):
        if self.children:
            print(self.children[0].Evaluate(symbolTable).value)


class Statement(Node):
    def __init__(self, children):
        super().__init__("", [])

    def Evaluate(self, symbolTable):
        for child in self.children:
            if symbolTable.get("retorne") is None:

                child.Evaluate(symbolTable)
            else:
                break


class Readline(Node):
    def __init__(self):
        super().__init__("", None)

    def Evaluate(self, symbolTable):
        self.value = int(input())
        return SymbolValue("int", self.value)


class While(Node):
    def __init__(self, value: str, children=[None, None]):
        if children and len(children) == 2:
            super().__init__(value, children)
        else:
            raise SyntaxError(
                f"INVALID OPERATION: WHILE must have 2 children ")

    def Evaluate(self, symbolTable):
        while (self.children[0].Evaluate(symbolTable).value or self.children[0].Evaluate(symbolTable).value != 0):
            if self.children[0].Evaluate(symbolTable).type == "str":
                raise SyntaxError(
                    f"INVALID OPERATION: type str is not a valid WHILE condition alone")
            else:
                self.children[1].Evaluate(symbolTable)


class IF(Node):
    def __init__(self, value: str, children):
        if children and len(children) >= 2:
            super().__init__(value, children)
        else:
            raise SyntaxError(
                f"INVALID OPERATION: IF must have 2 or 3 children ")

    def Evaluate(self, symbolTable):
        condition = self.children[0].Evaluate(symbolTable)
        if condition.type == "str":
            raise SyntaxError(
                f"INVALID OPERATION: type str is not a valid IF condition alone")
        if condition.value or condition.value != 0:
            self.children[1].Evaluate(symbolTable)
        else:
            if len(self.children) > 2 and self.children[2]:
                self.children[2].Evaluate(symbolTable)


class BoolVal(Node):
    def __init__(self, value: str):
        super().__init__(value, None)

    def Evaluate(self, symbolTable):
        return SymbolValue("bool", self.value)


class StringVal(Node):
    def __init__(self, value: str):
        super().__init__(value, None)

    def Evaluate(self, symbolTable):
        return SymbolValue("str", self.value)


class VarDec(Node):
    # value = None, children[0] = identifier_value (node: Identifier), children[1] = variable type (node: VarType)
    def __init__(self, value: str, children):
        if children and len(children) == 2:
            super().__init__(value, children)
        else:
            raise SyntaxError(
                f"INVALID OPERATION: node VarDec must have exactly 2 children ")

    def Evaluate(self, symbolTable):
        if self.children and len(self.children) == 2:
            symbolTable.declare_symbol(
                self.children[0].value, self.children[1].Evaluate())
        else:
            raise SyntaxError(
                f"INVALID OPERATION: node VarDec must have exactly 1 child ")


class VarType(Node):
    def __init__(self, value: str):  # value = variable type
        if value:
            self.value = value
        else:
            raise SyntaxError(
                f"INVALID OPERATION: node VarType must have a value ")

    def Evaluate(self):
        if self.value:
            return self.value
        else:
            raise SyntaxError(
                f"INVALID OPERATION: node VarType must have a value ")


class FuncDec(Node):
    # value = function name, children list of Symbol values
    def __init__(self, value: str, children, _type):  # value = variable type
        super().__init__(value, children)
        self.type = _type

    def Evaluate(self, symbolTable):
        symbolTable.declare_func(self.value, self.type, self)


class Return(Node):
    def __init__(self):
        super().__init__("RETURN", [])

    def Evaluate(self, symbolTable):
        symbolTable.set_symbol(
            "retorne", self.children[0].Evaluate(symbolTable))


class FuncCall(Node):
    # value = function name, children list of Symbol values
    def __init__(self, value: str):  # value = variable type
        super().__init__(value, [])

    def Evaluate(self, symbolTable):
        func_type, func_ref = symbolTable.get_func(self.value)
        new_st = Symbol_Table()
        if len(self.children) != (len(func_ref.children) - 1):
            raise Exception(
                f"INVALID OPERATION: numbers of arguments in function don't match: expected {len(self.children)} received {len(func_ref.children) - 1}")
        for i in range(len(func_ref.children)-1):
            value = self.children[i].Evaluate(symbolTable)
            arg_val, arg_type = func_ref.children[i]
            new_st.declare_symbol(arg_val, arg_type)
            new_st.set_symbol(arg_val, value)

        func_ref.children[-1].Evaluate(new_st)
        returnVal = new_st.get("retorne")
        if returnVal != None:
            if func_type == returnVal.type:
                return new_st.get("retorne")
            else:
                raise Exception(
                    f"INVALID OPERATION: return type don't match: expected {func_type} received {returnVal.type}")
