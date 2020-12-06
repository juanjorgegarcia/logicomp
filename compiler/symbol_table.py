from collections import namedtuple

SymbolValue = namedtuple("SymbolValue", "type, value")


class Symbol_Table:

    func_table = {}

    def __init__(self):
        self.symbols = {"retorne": None}

    def get(self, symbol):
        if symbol in self.symbols:
            return self.symbols[symbol]
        else:
            raise ValueError(
                f"INVALID ACCESS: there is no symbol: {symbol} in the Symbol Table{self.symbols}")

    def set_symbol(self, symbol, new_var):
        new_type, new_value = new_var
        if symbol in self.symbols:
            if symbol == "retorne":
                self.symbols[symbol] = new_var
            else:
                _type = self.symbols[symbol].type

                if self.check_types(new_value, _type) and new_type == _type:
                    self.symbols[symbol] = SymbolValue(
                        _type, new_value)
                else:
                    raise ValueError(
                        f"INVALID ASSIGNMENT: can't assign value {new_value} to variable of type {_type} ")

        else:
            raise ValueError(
                f"INVALID ASSIGNMENT: variable {symbol} is NOT declared in the Symbol Table {self.symbols}")

    def declare_symbol(self, symbol, _type):
        if symbol not in self.symbols and symbol not in Symbol_Table.func_table:
            self.symbols[symbol] = SymbolValue(_type, None)
        else:
            raise ValueError(
                f"INVALID DECLARATION: variable {symbol} already declared in the Symbol Table{self.symbols}")

    def check_types(self, value, _type):
        if _type == "bool":
            return self.is_boolean(value)
        elif _type == "int":
            return self.is_int(value)
        elif _type == "str":
            return self.is_str(value)

    def is_boolean(self, value):
        if value == True or value == False:
            return True
        else:
            return False

    def is_int(self, value):
        if isinstance(value, int):
            return True
        else:
            return False

    def is_str(self, value):
        if isinstance(value, str):
            return True
        else:
            return False

    def declare_func(self, symbol, _type, value):
        if symbol not in self.symbols and symbol not in Symbol_Table.func_table:
            Symbol_Table.func_table[symbol] = SymbolValue(_type, value)
        else:
            raise ValueError(
                f"INVALID DECLARATION: function {symbol} already declared in the Symbol Table{self.symbols} or in Function Table {Symbol_Table.func_table}")

    @staticmethod
    def get_func(func):
        if func in Symbol_Table.func_table:
            return Symbol_Table.func_table[func]
        else:
            raise ValueError(
                f"INVALID ACCESS: there is no function with the name: {func} in the Function Table{Symbol_Table.func_table}")
