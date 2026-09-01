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
            continue
            
        # Assume anything else is invalid
        return None # Parser should treat this as a tokenizing error
    
    tokens.append(("END", None))
    return tokens 

# We'll be going forward by keeping a state handy instead of anything Global

# Checks the current token
def current(state):
    return state["tokens"][state["pos"]]

# Consumes the current token, moves cursor (pos) to the next token in line
def eat(state, expected_type = None):
    token = state["tokens"][state["pos"]] # Track token
    if expected_type and token[0] != expected_type: 
        raise ValueError(f"Expected {expected_type}, received {token}")
    state["pos"] += 1 # Move cursor to the next token
    return token

# Primary parser
def parse_primary(state):
    token_type, token_val = current(state) # Get the current token.
                                           # Separate it into type of token, i.e. NUM, followed by the actual value that triggered it, i.e. "3.14"

    # Handling Numbers
    if token_type == "NUM": 
        eat(state)
        return ("num", float(token_val)) # Convert the raw string literal to a float value. Return a parse tree node tuple
                                         # formatted as, e.g. ("num", 3.14)

    # Handling parantheses
    elif token_type == "LPAREN":
        eat(state)
        # Apply recursion. 
        # Call the main expression parser, evaluate the whole math, then store into 'node' variable
        node = parse_expr(state)
        # Eat the token explicitly with a closing paranthesis. If the paranthesis isn't closed, an error is raised.
        eat(state, "RPAREN")
        return node
    else:
        raise ValueError("Invalid Syntax")

# Since exponentiation gets precedence above other operators,
def parse_power(state):
    left = parse_primary(state) # Get the immediately relevant left-hand node
    if current(state)[0] == "OP" and current(state)[1] == "^": 
        eat(state)
        right = parse_power(state) # Recursive call for a right associative
                                   # Simply, keep chaining to the right before completing the current node
        return ("bin", "^", left, right) # Format a suitable tuple to return
        # "bin" for binary, "^" for the operand, and link the 'left' and 'right' branches of exponentiation
    return left    

# Handle prefixes, with chaining allowed
def parse_unary(state):
    # As the check happens BEFORE reading a number, a unary operation (negation) is considered
    if current(state)[0] == "OP" and current(state)[1] == "-":
        eat(state)
        return ("neg", parse_unary(state)) # Recursively call on whatever follows to wrap the rest in the unary negation
    if current(state)[0] == "OP" and current(state)[1] == "+":
        raise ValueError ("Unary + disallowed.")
    return parse_power(state)

def parse_term(state):
    node = parse_unary(state) # After unary operation and exponentiation is considered, get left-hand operand
    while True: # Run an infinite loop
        token_type, token_val = current(state) # Get current token
        if token_type == "OP" and token_val in ("*", "/", "%"):
            eat(state)
            right = parse_unary(state) # Recursively call to wrap unary negation and get right-hand operand
            node = ("bin", token_val, node, right)
        elif token_type == "LPAREN":
            right = parse_unary(state)
            # For cases like 2(3), make sure the result is 6 emplopying Implicit Multiplication
            node = ("bin", "*", node, right)
            # Chain left-to-right by calling node
        else:
            break
    return node

# Handle + and - last
def parse_expr(state):
    node = parse_term(state) # Obtain left-hand operand
    while current(state)[0] == "OP" and current(state)[1] in ("+", "-"):
        op = current(state)[1] # Store the operand
        eat(state)
        right = parse_term(state) # Obtain right-hand operand
        node = ("bin", op, node, right)
        # To employ left-to-right chaining
    return node # Return the complete Abstract Syntax Tree for the entire expression


        
