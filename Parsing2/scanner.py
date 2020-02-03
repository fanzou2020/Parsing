# *****************************************************************************
# Author: Fan Zou
# A scanner to convert expression from text to logic token.
# The token can be any of these operators:
# /\   \/   ->   <->   ~
# They can also be the special symbols T and F, parentheses, variables

scannerConstant = {"EOF": "$"}

def scan(input):
    # Check that the input does not contain any invalid characters.
    # TODO: checkIntegerity(input)

    # Get a preliminary scan in which variables are named rather than numbered



