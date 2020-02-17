import parser
import truth_table

inputStr = input('Please enter the proposition:\n')
result = parser.parse(inputStr)
variables = result["variables"]

case = input('1. Given the truth value of variables.\n2. Generate truth table\n')

if case == '1':
    print("The variables are: ", end='')
    print(variables)
    s = input('please input the truth value of variables, using "true", "false", "T", or "F"\n')
    variableTokens = s.split(" ")
    # print(variableTokens)
    assignment = []
    for x in variableTokens:
        if x == 'true' or x == 'T':
            assignment.append(True)
        elif x == 'false' or x == 'F':
            assignment.append(False)

    print(assignment)
    ast = result["ast"].evaluate(assignment)
    print("The Value of this proposition is: ", end='')
    print(ast)

elif case == '2':
    print("The truth table of " + '"' + inputStr + '"')
    truth_table.generateTruthTable(result)




# variables = result["variables"]
#
# print(ast)
# print(variables)
#
# print()
#
# print("The truth table of " + '"' + inputStr + '"')
# truth_table.generateTruthTable(result)
