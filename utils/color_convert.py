class HexStringErrors:
    ERR_INVALID_STR_HASH = ValueError("Invalid hex string!\nHex string must begin with a # character.")
    ERR_INVALID_STR_CHARS = ValueError("Invalid hex string!\nHex string must only contain valid hex characters.")
    ERR_INVALID_STR_LEN = ValueError("Invalid hex string!\nHex code must be 3, 6, or 8 characters long.")

def convert_hex_string(hex_string):
    """
    Converts a hex string starting with '#' into an integer representation.

    :param hex_string: The input hex string, which must start with '#' and be 3, 6, or 8 characters long.
    :return: Integer representation of the processed hex string.
    :raises ValueError: If the hex string is invalid.
    """
    if not hex_string.startswith("#"):
        raise HexStringErrors.ERR_INVALID_STR_HASH

    trimmed = hex_string[1:]  # Remove the '#' character

    if len(trimmed) not in {3, 6, 8}:
        raise HexStringErrors.ERR_INVALID_STR_LEN

    if not all(c in "0123456789abcdefABCDEF" for c in trimmed):
        raise HexStringErrors.ERR_INVALID_STR_CHARS

    # Expand shorthand notation if length is 3 (e.g., #abc -> #aabbcc)
    def expand_shorthand(hex_parts):
        return [x * 2 if len(x) == 1 else x for x in hex_parts]

    # Split hex string into parts
    if len(trimmed) == 3:
        parts = [c for c in trimmed]
    else:
        parts = [trimmed[i:i+2] for i in range(0, len(trimmed), 2)]

    # Pad the alpha channel if missing
    if len(parts) == 3:
        parts.append("20")

    expanded_parts = expand_shorthand(parts)

    # Reverse parts and convert to integer
    reversed_parts = reversed(expanded_parts)
    combined = "".join(reversed_parts)

    return int(combined, 16)

# Example Usage
try:
    result = convert_hex_string("#9c67a0")
    print(f"Converted value: {result}")
except ValueError as e:
    print(f"Error: {e}")
