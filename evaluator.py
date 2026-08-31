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