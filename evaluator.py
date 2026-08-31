"""
evaluator.py — HIT137 Assignment 2, Question 2

Basic:
Use plain functions to build a fully functional evaluator
with recurisve descent parsing. It reads expressions from
the given input file (one at a time), then parses and 
evaluates each expression according to defined operator
presedence, then writes to output.txt.

Base requirements:
1) Handle five binary operators (+, -, *, /, %)
2) Handle exponentiation
3) Handle paranthesis (any nest depth)
4) Unary negation
5) Unary + unsupported, produce error
6) Unary negation may appear at start of an operation, after 
   an opening paranthesis or after any operator
7) Implicit Multiplication is a valid expression

For each expression, output:
1) The original expression 
2) Parse tree representation
3) Tokenizing 
4) Computed results or errors


Basic formatting:
Results are formatted such that whole numbers are displayed
without any decimal points, whereas non-integers are defaulted
to 4 decimal places.
"""

def tokenizer(expr: str):
    tokens = []
    i = 0 # Cursor position in the expression / Index
    n = len(expr)
    
    while i < n:
        char = expr[i] # Iterate through each character in the expression
        
        
        # Skip if whitespace
        if char.isspace():
            i += 1 
            continue
        
        # For digits
        if char.isdigit():
            start = i # Remember where the number began
            while i < n and expr[i].isdigit():
                i += 1 
            # Handle decimals
            if i < n and expr[i] == ".":
                i += 1
                if i >= n or not expr[i].isdigit(): # If after the "." there ISN'T a digit,
                    return None # It's not a decimal.
                while i < n and expr[i].isdigit(): #If after the "." there IS a digit
                    i += 1 # Treat as a decimal
            # Since 'start' marks the posiition where the number started
            # and i marks the position of the cursor of the latest number
            # Simply pass them as starting and ending values
            tokens.append(("NUM", expr[start: i]))
            continue

        # For Operands
        if char in "+-*/%":
            tokens.append(("OP", char))
            i += 1
            continue

        # For Parantheses
        if char == "(":
            tokens.append(("LPAREN", "(")) 
            i += 1
            continue
        
        if char == ")":
            tokens.append(("RPAREN", ")")) 
            i += 1
            continuez
            
        # Assume anything else is invalid
        return None # Parser should treat this as a tokenizing error
    
    tokens.append(("END", None))
    return tokens 
    console.log(tokens)
    
tokenizer("3 + 5 = (8)")

