import parser
import truth_table

inputStr = input('Please enter the proposition:\n')
assignment = [True, False, True, False]
result = parser.parse(inputStr)
ast = result["ast"].evaluate(assignment)
variables = result["variables"]

print(ast)
print(variables)

print()

print("The truth table of " + '"' + inputStr + '"')
truth_table.generateTruthTable(result)
