# ******************************************************************************
# All ast (abstract syntax tree) nodes must have functions of the form
#   evaluate(assignment), returns the value of the expression given the
#                         variable assignment as an array of trues and falses.
#


# *** Node type for T ***
class TrueNode:
    def evaluate(self, assignment):
        return True


# *** Node type for F ***
class FalseNode:
    def evaluate(self, assignment):
        return False


# *** Node type for ~ ***
class NegateNode:
    def __init__(self, underlying):
        self.underlying = underlying

    def evaluate(self, assignment):
        return not self.underlying.evaluate(assignment)


# *** Node type for and /\ ***
class AndNote:
    def __init__(self, lhs, rhs):
        self.lhs = lhs
        self.rhs = rhs

    def evaluate(self, assignment):
        return self.lhs.evaluate(assignment) and self.rhs.evaluate(assignment)


# *** Node type for or \/ ***
class OrNode:
    def __init__(self, lhs, rhs):
        self.lhs = lhs
        self.rhs = rhs

    def evaluate(self, assignment):
        return self.lhs.evaluate(assignment) or self.rhs.evaluate(assignment)


# *** Node type for -> ***
class ImpliesNode:
    def __init__(self, lhs, rhs):
        self.lhs = lhs
        self.rhs = rhs

    def evaluate(self, assignment):
        return (not self.lhs.evaluate(assignment)) or self.rhs.evaluate(assignment)


# *** Node type for <-> ***
class IffNode:
    def __init__(self, lhs, rhs):
        self.lhs = lhs
        self.rhs = rhs

    def evaluate(self, assignment):
        return self.lhs.evaluate(assignment) == self.rhs.evaluate(assignment)


# *** Node type for variables ***
class VariableNode:
    def __init__(self, index):
        self.index = index

    def evaluate(self, assignment):
        return assignment[self.index]

# assignment = [True, False, True, False]
# variables = ["P1", "P2", "P3", "P4"]
# t1 = TrueNode()
# t2 = FalseNode()
# t3 = TrueNode()
# t4 = FalseNode()
# a = IffNode(t1, t2)
# b = NegateNode(t3)
# print(a.evaluate(assignment))
# print(a.toString(variables))
# print(b.evaluate(assignment))
# print(b.toString(assignment))
