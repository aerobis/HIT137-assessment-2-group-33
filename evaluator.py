import os
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
        if char in "+-*/%^":
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

# ============================================================
# HIMANSHU PART - EVALUATION AND OUTPUT FORMATTING
# ============================================================

# Evaluates the parse tree and returns the final answer
def evaluate_tree(node):
    kind = node[0]

    # If the node is just a number, return its value
    if kind == "num":
        return node[1]

    # Handle negative values
    if kind == "neg":
        return -evaluate_tree(node[1])

    # Handle binary operations such as +, -, *, /, %, ^
    if kind == "bin":
        op = node[1]

        # Evaluate both sides of the operation first
        left = evaluate_tree(node[2])
        right = evaluate_tree(node[3])

        if op == "+":
            return left + right

        elif op == "-":
            return left - right

        elif op == "*":
            return left * right

        elif op == "/":
            return left / right

        elif op == "%":
            return left % right

        elif op == "^":
            return left ** right

    # This should only happen if the tree is invalid
    raise ValueError("Invalid expression tree")


# Formats the number before writing it to output.txt
def format_number(value):

    # Remove .0 from whole numbers, for example 8.0 becomes 8
    if value == int(value):
        return str(int(value))

    # Round decimal answers to a maximum of 4 decimal places
    return str(round(value, 4))


# Changes the parse tree into the format required by the assignment
def tree_to_string(node):
    kind = node[0]

    # Number nodes are displayed normally
    if kind == "num":
        return format_number(node[1])

    # Unary negative is displayed using "neg"
    if kind == "neg":
        return "(neg " + tree_to_string(node[1]) + ")"

    # Binary operations are displayed as (operator left right)
    if kind == "bin":
        op = node[1]

        left = tree_to_string(node[2])
        right = tree_to_string(node[3])

        return "(" + op + " " + left + " " + right + ")"

    raise ValueError("Invalid expression tree")


# Converts the token list into the required output format
def tokens_to_string(tokens):
    parts = []

    for token_type, token_value in tokens:

        # END token does not have a value
        if token_type == "END":
            parts.append("[END]")

        else:
            parts.append(
                "[" + token_type + ":" + token_value + "]"
            )

    # Put one space between each token
    return " ".join(parts)


# Handles one expression from start to finish
def process_expression(expr):

    # First convert the expression into tokens
    tokens = tokenizer(expr)

    # Invalid characters cause a tokenizing error
    if tokens is None:
        return {
            "input": expr,
            "tree": "ERROR",
            "tokens": "ERROR",
            "result": "ERROR"
        }

    token_text = tokens_to_string(tokens)

    # Try to parse the expression and create its tree
    try:
        state = {
            "tokens": tokens,
            "pos": 0
        }

        tree = parse_expr(state)

        # After parsing, only the END token should remain
        if current(state)[0] != "END":
            raise ValueError("Unexpected token")

        tree_text = tree_to_string(tree)

    # If parsing fails, return an error for the expression
    except (ValueError, IndexError):
        return {
            "input": expr,
            "tree": "ERROR",
            "tokens": token_text,
            "result": "ERROR"
        }

    # The expression may parse correctly but still fail while calculating
    # For example: 1 / 0
    try:
        result = float(evaluate_tree(tree))

    except (ZeroDivisionError, ValueError, OverflowError):
        result = "ERROR"

    return {
        "input": expr,
        "tree": tree_text,
        "tokens": token_text,
        "result": result
    }


# Main function required by the assignment
def evaluate_file(input_path: str) -> list[dict]:
    results = []

    # Read all expressions from the input file
    with open(input_path, "r") as input_file:
        expressions = input_file.read().splitlines()

    # Process each expression one at a time
    for expression in expressions:
        result = process_expression(expression)
        results.append(result)

    # Create output.txt in the same folder as the input file
    output_dir = os.path.dirname(input_path)
    output_path = os.path.join(output_dir, "output.txt")

    blocks = []

    # Build the four required output lines for each expression
    for item in results:

        if item["result"] == "ERROR":
            result_text = "ERROR"

        else:
            result_text = format_number(item["result"])

        block = (
            "Input: " + item["input"] + "\n"
            "Tree: " + item["tree"] + "\n"
            "Tokens: " + item["tokens"] + "\n"
            "Result: " + result_text
        )

        blocks.append(block)

    # Separate each expression block with a blank line
    with open(output_path, "w") as output_file:
        output_file.write("\n\n".join(blocks))

    return results


# Run the program using input.txt when this file is executed directly
if __name__ == "__main__":
    evaluate_file("input.txt")