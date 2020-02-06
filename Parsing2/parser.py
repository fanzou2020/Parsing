# *****************************************************************
# A parser that produces an AST from a sequence of tokens
from Parsing2 import scanner
from Parsing2 import ast


# Given input, parse it to generate AST and variable map.
# The returned dictionary have two parts:
#    "ast"      : The root of generated AST.
#    "variables": A map from indices to variables.

def parse(inputStr):
    scanResult = scanner.scan(inputStr)
    tokens = scanResult["tokens"]

    # Use Dijkstra's shunting-yard algorithm. There are two stacks, one
    # is operator stack, one is operand stack which also include left parentheses.
    #
    # To deal with ~ operator, we push it onto the operator stack, when we read an
    # operand, we repeatedly pop  off negations until none remain.

    operators = []
    operands = []

    # if true, we are expecting an operand, else, we need an operator
    needOperand = True

    # Scan through the tokens
    for currToken in tokens:
        if (needOperand):
            # if is an operand, push it on the operand stack
            if isOperand(currToken):
                addOperand(wrapOperand(currToken), operands, operators)
                needOperand = False

            # if it is a parenthesis or negation, push it on operator stack.
            elif currToken["type"] == '(' or currToken["type"] == '~':
                operators.append(currToken)

            elif currToken["type"] == scanner.scannerConstantEOF:
                # if the operator stack is empty, the input was empty
                if len(operators) == 0:
                    parseError("", 0, 0)

                # if the operator stack has an ( on top, it is unmatched
                if topOf(operators)["type"] == '(':
                    parseError("Open parenthesis has no matching close parenthesis",
                               topOf(operators)["start"], topOf(operators)["end"])

                # otherwise, it is an operator with no operand.
                parseError("This operator is missing an operand",
                           topOf(operators)["start"], topOf(operators)["end"])

            else:
                parseError("We are excepting a variable", currToken["start"], currToken["end"])

        # We are expecting either an operator or a close parenthesis
        else:
            if (isBinaryOperator(currToken)) or currToken["type"] == scanner.scannerConstantEOF:
                # While there are high priority operators at the top of stack, evaluate them first.
                while True:
                    if len(operators) == 0:
                        break

                    if topOf(operators)["type"] == '(':
                        break

                    if priorityOf(topOf(operators)) <= priorityOf(currToken):
                        break

                    # only if priority of top of operators is greater than current token,
                    # evaluate them first
                    operator = operators.pop()
                    rhs = operands.pop()
                    lhs = operands.pop()

                    addOperand(createOperatorNode(lhs, operator, rhs), operands, operators)

                # push this operator onto the operators stack.
                operators.append(currToken)

                #
                needOperand = True

                if currToken["type"] == scanner.scannerConstantEOF:
                    break

            # If this is a close parenthesis, we pop operators from the stack and evaluate
            # them until an open parenthesis. Then still search for an operator
            elif currToken["type"] == ')':
                # keep popping operators until "("
                while True:
                    if len(operators) == 0:
                        parseError("This '(' dones not match any ')')", currToken["start"], currToken["end"])

                    currOp = operators.pop()

                    if currOp["type"] == '(':
                        break

                    if currOp["type"] == '~':
                        parseError("Nothing is negated by this operator.", currToken["start"], currToken["end"])

                    # otherwise, it should be an operator, evaluate it.
                    rhs = operands.pop()
                    lhs = operands.pop()

                    addOperand(createOperatorNode(lhs, currOp, rhs), operands, operators)

                # expose to negations.
                expr = operands.pop()
                addOperand(expr, operands, operators)

            # Anything else is an error
            else:
                parseError("Expecting a close parenthesis or a binary operator here",
                           currToken["start"], currToken["end"])

    # Successfuly parsed the input string
    # TODO: The operator stack should be empty. Check such errors.

    return {
        "ast": operands.pop(),
        "variables": scanResult["variables"]
    }


# Whether the operator is binary operator
def isBinaryOperator(token):
    return token["type"] == "<->" or token["type"] == "->" or token["type"] == "/\\" \
           or token["type"] == "\\/"


# Whether the given token is an operand. The operands are T, F and variables
def isOperand(token):
    return token["type"] == "T" or token["type"] == "F" or token["type"] == "variable"


# Given an operand token, return an AST node
def wrapOperand(token):
    if token["type"] == "T":
        return ast.TrueNode()

    if token["type"] == "F":
        return ast.FalseNode()

    if token["type"] == "variable":
        return ast.VariableNode(token["index"])


# Add a new operand to operand stack, if any negations need to be perform first,
# evaluate them.
def addOperand(node, operands, operators):
    # keep evaluating "~" until none remain.
    while len(operators) > 0 and topOf(operators)["type"] == "~":
        operators.pop()
        node = ast.NegateNode(node)

    # after negating the node, push it back to operands stack
    operands.append(node)


# priorityOf operators.
def priorityOf(token):
    if token["type"] == scanner.scannerConstantEOF:
        return -1
    if token["type"] == "<->":
        return 0
    if token["type"] == "->":
        return 1
    if token["type"] == "\\/":
        return 2
    if token["type"] == "/\\":
        return 3


# Create operator AST node.
def createOperatorNode(lhs, token, rhs):
    if token["type"] == "<->":
        return ast.IffNode(lhs, rhs)
    if token["type"] == "->":
        return ast.ImpliesNode(lhs, rhs)
    if token["type"] == "\\/":
        return ast.OrNode(lhs, rhs)
    if token["type"] == "/\\":
        return ast.AndNote(lhs, rhs)


# return the top of stack.
def topOf(array):
    if len(array) == 0:
        return None
    else:
        return array[len(array) - 1]


# parseError
def parseError(why, start, end):
    raise Exception(why + "start " + str(start) + "end " + str(end))
