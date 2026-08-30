"""
cipher.py — HIT137 Assignment 2, Question 1

Encrypts/decrypts raw_text.txt using a custom substitution cipher.

Rules (per assignment spec):
  Lowercase a-n : shift forward by shift1 * shift2
  Lowercase o-z : shift backward by shift1 + shift2
  Uppercase A-M : shift backward by shift1
  Uppercase N-Z : shift forward by shift2 ** 2
  Digits   0-9  : shift forward by shift1 - shift2
  Everything else (spaces, punctuation, etc.) is left unchanged.

Approach:
  Each shift wraps AROUND WITHIN ITS OWN SUB-RANGE (a-n, o-z, A-M, N-Z,
  0-9) rather than around the full 26-letter alphabet. This keeps every
  shifted character in the same category it started in, which makes the
  cipher a clean bijection on each sub-range -- so decryption (the exact
  mirror shift) always recovers the original text, no matter how large
  shift1/shift2 are. (If shifts wrapped around the full alphabet instead,
  a letter from one half could land in the other half's territory,
  making some encryptions impossible to reverse -- so wrapping within
  the sub-range is the only design that keeps encrypt/decrypt/verify
  consistent for all valid inputs.)

  We build an explicit substitution table for every possible input
  character based on the ORIGINAL character's position, then decrypt by
  inverting that same table.
"""

LOWER_FIRST_HALF = "abcdefghijklmn"   # a-n (14 letters)
LOWER_SECOND_HALF = "opqrstuvwxyz"    # o-z (12 letters)
UPPER_FIRST_HALF = "ABCDEFGHIJKLM"    # A-M (13 letters)
UPPER_SECOND_HALF = "NOPQRSTUVWXYZ"   # N-Z (13 letters)


def _build_encryption_table(shift1: int, shift2: int) -> dict:
    """Builds a dict mapping every relevant plaintext character to its
    encrypted counterpart, based on the assignment's shifting rules."""
    table = {}

    # Lowercase letters (each half wraps within its own length: 14 or 12)
    for i, ch in enumerate(LOWER_FIRST_HALF):
        new_i = (i + shift1 * shift2) % 14
        table[ch] = LOWER_FIRST_HALF[new_i]
    for i, ch in enumerate(LOWER_SECOND_HALF):
        new_i = (i - (shift1 + shift2)) % 12
        table[ch] = LOWER_SECOND_HALF[new_i]

    # Uppercase letters (each half wraps within its own length: 13 or 13)
    for i, ch in enumerate(UPPER_FIRST_HALF):
        new_i = (i - shift1) % 13
        table[ch] = UPPER_FIRST_HALF[new_i]
    for i, ch in enumerate(UPPER_SECOND_HALF):
        new_i = (i + shift2 ** 2) % 13
        table[ch] = UPPER_SECOND_HALF[new_i]

    # Digits
    for d in range(10):
        new_d = (d + (shift1 - shift2)) % 10
        table[str(d)] = str(new_d)

    return table


def _apply_table(text: str, table: dict) -> str:
    """Applies a substitution table to text; characters not in the
    table (spaces, punctuation, newlines, etc.) pass through unchanged."""
    return "".join(table.get(ch, ch) for ch in text)


def encrypt_file(shift1: int, shift2: int, input_path: str, output_path: str) -> None:
    """Reads input_path, encrypts its contents, writes to output_path."""
    table = _build_encryption_table(shift1, shift2)
    with open(input_path, "r", encoding="utf-8") as f:
        content = f.read()
    encrypted = _apply_table(content, table)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(encrypted)


def decrypt_file(shift1: int, shift2: int, input_path: str, output_path: str) -> None:
    """Reads input_path (encrypted text), decrypts it, writes to output_path."""
    forward_table = _build_encryption_table(shift1, shift2)
    # Invert the table so we can map encrypted chars back to originals.
    reverse_table = {v: k for k, v in forward_table.items()}
    with open(input_path, "r", encoding="utf-8") as f:
        content = f.read()
    decrypted = _apply_table(content, reverse_table)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(decrypted)


def verify_files(original_path: str, decrypted_path: str) -> bool:
    """Compares original_path with decrypted_path, prints and returns
    whether they match exactly."""
    with open(original_path, "r", encoding="utf-8") as f:
        original = f.read()
    with open(decrypted_path, "r", encoding="utf-8") as f:
        decrypted = f.read()

    success = original == decrypted
    if success:
        print("Verification successful: decrypted text matches the original.")
    else:
        print("Verification FAILED: decrypted text does not match the original.")
    return success


def _get_non_negative_int(prompt: str) -> int:
    """Prompts the user until they enter a valid non-negative integer."""
    while True:
        raw = input(prompt)
        try:
            value = int(raw)
            if value < 0:
                print("Please enter a non-negative integer.")
                continue
            return value
        except ValueError:
            print("Please enter a valid integer.")


def main() -> None:
    shift1 = _get_non_negative_int("Enter shift1 (non-negative integer): ")
    shift2 = _get_non_negative_int("Enter shift2 (non-negative integer): ")

    raw_path = "raw_text.txt"
    encrypted_path = "encrypted_text.txt"
    decrypted_path = "decrypted_text.txt"

    encrypt_file(shift1, shift2, raw_path, encrypted_path)
    print(f"Encrypted '{raw_path}' -> '{encrypted_path}'")

    decrypt_file(shift1, shift2, encrypted_path, decrypted_path)
    print(f"Decrypted '{encrypted_path}' -> '{decrypted_path}'")

    verify_files(raw_path, decrypted_path)


if __name__ == "__main__":
    main()