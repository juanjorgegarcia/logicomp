from _parser import Parser
import sys
from symbol_table import *

with open(sys.argv[1], 'r') as f:
    output = f.read()
table = Symbol_Table()
Parser.run(output).Evaluate(table)
