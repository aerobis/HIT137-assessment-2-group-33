# HIT137 Assessment 2 Group DAN/EXT 33

# Group Members:
### Sobit Paudel          - S403784 - Question 1 cipher.py

### Shreyash Upreti       - S406921 - Question 2 Tokenizer And Parser

### Himanshu Bhattarai    - S407972 - Question 2 Evaluation And Formatting

### Waraphorn Boonprawat  - S402989 - Question 2 Testing And  Implementation 

Group assignment for HIT137 (Software Now), covering two independent programs:
1) cipher.py:
   A program that acts as a custom substitution cypher. Encrypts and decrypts raw_text.txt using position dependent shifts with varying rules for lowercase a-n / o -z, uppercase A-M / N-Z and digits, then verifies the round trip.

2) evaluator.py
   A recersive-descent arithmetic expression evaluator. Reads expressions from input.txt, tokenizes and then parses them into a tree, evaluates the results, and writes it to an output.txt

# HOW TO RUN
### Cipher (Q1, cipher.py):
Prompts for Shift1 and Shift2 (non-negative integers). Reads raw_text.txt and produces encrypted_text.txt and decrypted_text.txt, printing whether verification succeeded.

### Evaluator (Q2, evaluator.py):
Reads input.txt (one expression per line), writes output.txt in the same directory with completed Input/Tree/Tokens/Result block for each expression

# DESIGN NOTES
cipher.py shifts each character *within its own sub-range* (a-n, o-z, A-M, N-Z, 0-9) rather than around the full 26 letter alphabet. This is so it can keep every shifted character in the same category it started in, making the implementation cleaner, making sure decryption always recovers the original text with no errors.

### INPUTS FOR Q1:
SHIFT 1 => 5
SHIFT 2 => 29