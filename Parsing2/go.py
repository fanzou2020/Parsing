from Parsing2 import parser
from Parsing2 import truth_table

inputStr = "~(a and b) -> c"
assignment = [True, False, True, False]
result = parser.parse(inputStr)
ast = result["ast"].evaluate(assignment)
variables = result["variables"]

print(ast)
print(variables)

print()

print("The truth table of " + '"' + inputStr + '"')
truth_table.generateTruthTable(result)
