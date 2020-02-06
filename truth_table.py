# **********************************************************************
# Generate truth table, go through


def generateTruthTable(parseResult):
    numOfVarialbes = len(parseResult["variables"])
    assignment = []
    for i in range(numOfVarialbes):
        assignment.append(False)

    while True:
        print(assignment, end='')
        print("  =  ", end='')
        print(parseResult["ast"].evaluate(assignment))

        if not nextAssignment(assignment):
            break


# return true if we have not go through all possibilities.
# and change to assignment list to the next possibility.
def nextAssignment(assignment):
    # Walking from the right to left, search for a false to make it true.
    flip_index = len(assignment) - 1
    while flip_index >= 0 and assignment[flip_index]:
        flip_index -= 1

    # If we didn't find an index to flip, we've tried all possibilities, and therefore are done.
    if flip_index == -1:
        return False

    # Otherwise, flip this index to true and all following values to false.
    assignment[flip_index] = True
    for i in range(flip_index + 1, len(assignment)):
        assignment[i] = False

    return True