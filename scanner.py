# *****************************************************************************
# A scanner to convert expression from text to logic token.
# The token can be any of these operators:
# /\   \/   ->   <->   ~
# They can also be the special symbols T and F, parentheses, variables
import re

scannerConstantEOF = "$"


# Scans the inputStr and produces an dictionary with two fields:
#
#       "tokens":     A list of tokens in the input, in order
#       "variables":  A list of the variables sorted by alphabetical order,
#                     keyed by their index.
#
def scan(inputStr):
    # Check that the input does not contain any invalid characters.
    # TODO: checkIntegerity(input)

    # Get a preliminary scan in which variables are named rather than numbered
    preliminary = preliminaryScan(inputStr)

    # Convert the preliminary scan into the result by sorting variables by name
    # and renumbering them
    return numberVariables(preliminary)
#    return preliminary


# Does a preliminary scan of the input. The preliminary scan is identical to
# the final scan, except that the variables are named rather than numbered.
# The returned dictionary will have two fields:
#
#      "tokens":      The tokens in the input.
#      "variableSet": A dictionary of all the tokens named in the input.
#
def preliminaryScan(inputStr: str):
    # Append the $ marker to the end of input, this means a EOF marker.
    inputStr += scannerConstantEOF

    # Run the scan
    i = 0  # index
    variableSet = {}  # Set of variables
    tokens = []  # List of tokens

    while True:
        curr = inputStr[i]

        # Stop on EOF if we find it
        if curr == scannerConstantEOF:
            tokens.append(makeIdentityToken(curr, i))
            return {"tokens": tokens,
                    "variableSet": variableSet}

        # reading a variable
        elif isVariableStart(inputStr, i):
            variable = scanVariable(inputStr, i, variableSet)
            tokens.append(makeVariableToken(variable, i))

            # skip past the token characters
            i += len(variable)

        # if we are reading an operator or other syntax
        elif isOperatorStart(inputStr, i):
            token = tryReadOperator(inputStr, i)
            tokens.append(makeIdentityToken(token, i))

            # skip the characters we just read
            i += len(token)

        elif isWhitespace(inputStr[i]):
            i += 1

        else:
            print("The character " + inputStr[i] + " should not be here.", i, i + 1)


#
def isOperatorStart(inputStr, i):
    return tryReadOperator(inputStr, i) is not None


#
def tryReadOperator(inputStr, i):
    # Case 1: single-char operator like, (, ), ~, T, F, !
    if re.match(r'[()~TF!]', inputStr[i]):
        return inputStr[i]

    # Case 2: Two-char operator like ->, \/, /\, =>, or, &&, ||
    if i == len(inputStr) - 1:
        return None
    twoChars = inputStr[i:i + 2]
    twoCharsSet = {"/\\", "\\/", "->", "=>", "&&", "||", "or"}
    if twoChars in twoCharsSet:
        return twoChars

    # Case 3: Three-char operator like <-> <=>
    if i == len(inputStr) - 2:
        return None
    threeChars = inputStr[i:i + 3]
    threeCharsSet = {"<->", "<=>", "and", "not", "iff"}
    if threeChars in threeCharsSet:
        return threeChars

    # Case 4: Four-char operator like "true", "True"
    if i == len(inputStr) - 3:
        return None
    fourChars = inputStr[i:i + 4]
    if fourChars == "true":
        return fourChars

    # Case 5: Five-char operator like "false"
    if i == len(inputStr) - 4:
        return None
    fiveChars = inputStr[i:i + 5]
    if fiveChars == "false":
        return fiveChars

    # Case 6: Seven-char operator like "implies"
    if i == len(inputStr) - 6:
        return None
    sevenChars = inputStr[i:i + 7]
    if sevenChars == "implies":
        return sevenChars

    # Others, nothing matched
    return None


# Determines whether the input beginning at the name of variable
def isVariableStart(inputStr, i):
    return tryReadVariableName(inputStr, i) is not None


#
def tryReadVariableName(inputStr, i):
    # variables should start with a letter or underscore.
    if not re.match(r'[A-Za-z_0-9]', inputStr[i]):
        return None

    # Keep reading characters while it is possible to do so.
    result = ''
    while re.match(r'[A-Za-z_0-9]', inputStr[i]):
        result += inputStr[i]
        i += 1

    # Return the result as long as it is not a reserved word
    if isReservedWord(result):
        return None
    else:
        return result


# Returns whether the token is a reserved word.
def isReservedWord(result):
    reservedWordSet = {"T", "F", "and", "or", "not", "iff", "implies", "true", "false"}
    return result in reservedWordSet


#
def scanVariable(inputStr, i, variableSet):
    variableName = tryReadVariableName(inputStr, i)

    variableSet[variableName] = True
    return variableName


# wrap the variable with a token for the scanner
def makeVariableToken(variable: str, i: int):
    return {
        "type": "variable",
        "index": variable,
        "start": i,
        "end": i + len(variable)
    }


# warps the string up as a token for the scanner
def makeIdentityToken(curr: str, i: int):
    return {
        "type": translate(curr),
        "start": i,
        "end": i + len(curr)
    }


# Translate equivalent token to and, or, implies, etc..
def translate(curr: str):
    if (curr == "&&") or (curr == "and"):
        return "/\\"
    if (curr == "||") or (curr == "or"):
        return "\\/"
    if (curr == "=>") or (curr == "implies"):
        return "->"
    if (curr == "<=>") or (curr == "iff"):
        return "<->"
    if (curr == "not") or (curr == "!"):
        return "~"
    if curr == "true":
        return "T"
    if curr == "false":
        return "F"
    return curr


# Check if it it white space
def isWhitespace(char):
    if re.match(r'\s+', char):
        return True
    return False


# Given the result of a preliminary scan, sorts the variables and renumbers them alphabetically
# The returned object has two fields:
#       tokens:     The tokens from the scan, with variables numbered.
#       variables:  An array mapping numbers to variable names.
def numberVariables(preliminary):
    variables = []
    for key in preliminary["variableSet"]:
        variables.append(key)

    # Sort the variables alphabetically
    variables.sort()

    # Change the variables in variableSet from variable name to integer index.
    for i in range(len(variables)):
        preliminary["variableSet"][variables[i]] = i

    # Change the "index" parameter in tokens form variable name to integer index.
    for j in range(len(preliminary["tokens"])):
        if preliminary["tokens"][j]["type"] == "variable":
            preliminary["tokens"][j]["index"] = preliminary["variableSet"][preliminary["tokens"][j]["index"]]

    return {
        "tokens": preliminary["tokens"],
        "variables": variables
    }



# inputStr = "P1 and ((P2 or P3) \/ !P45) and T or F"
# scannerResult = scan(inputStr)
# tokens = scannerResult["tokens"]
# variables = scannerResult["variables"]
# for x in tokens:
#     print(x)
# for y in variables:
#     print(y)

