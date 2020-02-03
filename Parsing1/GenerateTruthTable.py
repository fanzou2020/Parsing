from Parsing1 import Parsing as ps


# create a new array of truth values of each possibility for n variables.
# initialize the array with all false values.
def generate_truth_table(sentence_list: list, num_of_var: int):

    assignment = []
    for i in range(num_of_var):
        assignment.append(False)

    while True:
        dictionary = generate_dict(num_of_var, assignment)
        print(assignment, end='')
        print("  =  ", end='')
        print(ps.parsing(sentence_list, dictionary))

        if not next_assignment(assignment):
            break


# generate dictionary like {"P1": True, "P2": False, ..., "Pn": True}
# using the values of assignment list [True, False, ..., True]
def generate_dict(num_of_var, assignment):
    dictionary = {}
    for i in range(num_of_var):
        dictionary["P" + str(i + 1)] = assignment[i]

    return dictionary


# return true if we have not go through all possibilities.
# and change to assignment list to the next possibility.
def next_assignment(assignment):
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

