from typing import List
from base64 import b64encode, b64decode
from re import sub
from json import dumps, loads

def string_to_ascii(string: str, static_num: int = 0) -> List[int]:
    """
    Convert a string to a list of ASCII values using a static number.

    Args:
        string: The string to convert to ASCII values.
        static_num: A static number to XOR each ASCII value with. Default is 0.

    Returns:
        A list of ASCII values.
    """
    return [ord(char) ^ static_num for char in string]

def ascii_to_string(ascii_list: List[int], static_num: int = 0) -> str:
    """
    Convert a list of ASCII values to a string using a static number.

    Args:
        ascii_list: The list of ASCII values to convert to a string.
        static_num: A static number to XOR each ASCII value with. Default is 0.

    Returns:
        The resulting string.
    """
    return "".join([chr(ascii ^ static_num) for ascii in ascii_list])

def ascii_to_base64(ascii_list: List[int]) -> str:
    """
    Convert a list of ASCII values to a base64 string.

    Args:
        ascii_list: The list of ASCII values to convert to a base64 string.

    Returns:
        The resulting base64 string.
    """
    return b64encode(bytes(ascii_list)).decode("utf-8")

def base64_to_ascii(base64_string: str) -> List[int]:
    """
    Convert a base64 string to a list of ASCII values.

    Args:
        base64_string: The base64 string to convert to a list of ASCII values.

    Returns:
        A list of ASCII values.
    """
    return list(b64decode(base64_string))

def swap(ascii_list: List[int]) -> List[int]:
    """
    Swaps every two adjacent elements in a list.

    Args:
        ascii_list: The list of ASCII values to swap.

    Returns:
        A new list with every two adjacent elements swapped.
    """
    for i in range(0, len(ascii_list) - 1, 2):
        ascii_list[i], ascii_list[i+1] = ascii_list[i+1], ascii_list[i]
    return ascii_list

def swap_back(ascii_list: List[int]) -> List[int]:
    """
    Swaps every two adjacent elements in a list back to the original order.

    Args:
        ascii_list: The list of ASCII values to swap back.

    Returns:
        A new list with every two adjacent elements swapped back.
    """
    return swap(ascii_list)

def xor_shift(ascii_list: List[int], key: List[int], n: int=0) -> List[int]: 
    """
    Performs a byte-level shift and XOR operation on a list of ASCII values.

    Args:
        ascii_list: The list of ASCII values to transform.
        key: The list of integers to XOR with each value in `ascii_list`.
        n: The index of the key to use for the shift. Default is 0.

    Returns:
        A new list of transformed ASCII values.
    """
    shift = key[n] % 7 + 1
    return [(c << shift | c >> 8 - shift) & 255 for c in ascii_list]
    
def xor_unshift(ascii_list: List[int], key: List[int], n: int=0) -> List[int]:
    """
    Performs the inverse of a byte-level shift and XOR operation on a list of ASCII values.

    Args:
        ascii_list: The list of ASCII values to transform back to the original order.
        key: The list of integers to XOR with each value in `ascii_list`.
        n: The index of the key to use for the shift. Default is 0.

    Returns:
        A new list of ASCII values in the original order.
    """
    shift = key[n] % 7 + 1
    return [(c >> shift | c << 8 - shift) & 255 for c in ascii_list]

def interleave(ascii_list: List[int], key: int, start: List[int], end: int) -> List[int]: 
    """
    Interleaves two lists of ASCII values by taking one value from each list at a time.

    Args:
        ascii_list: The first list of ASCII values to interleave.
        key: The second list of ASCII values to interleave.


    Returns:
        A new list of interleaved ASCII values.
    """
    return [val for pair in zip(ascii_list, key[start:end]) for val in pair]

def deinterleave(interleaved_list: List[int], key: List[int]) -> List[int]:
    """
    Reverses the interleaving of two lists of ASCII values.

    Args:
        ascii_list: The list of interleaved ASCII values to transform back to the original order.
        key: The second list of ASCII values used to interleave the first list.

    Returns:
        A new list of ASCII values in the original order.
    """
    return interleaved_list[::2]

def rotate(ascii_list: List[int], key: List[int], n: int) -> List[int]: 
    """
    Rotates a list of ASCII values by a given amount.

    Args:
        ascii_list: The list of ASCII values to rotate.
        key: The list of integers to use as rotation offsets.
        n: The index of the key to use for the rotation.

    Returns:
        A new list of rotated ASCII values.
    """
    return [ascii_list[(i+key[n]) % len(ascii_list)] for i in range(len(ascii_list))]

def unrotate(ascii_list: List[int], key: List[int], n: int) -> List[int]: 
    """
    Reverses the rotation of a list of ASCII values by a given amount.

    Args:
        ascii_list: The list of rotated ASCII values to transform back to the original order.
        key: The list of integers used as rotation offsets.
        n: The index of the key used for the rotation.

    Returns:
        A new list of ASCII values in the original order.
    """
    return [ascii_list[(i - key[n] + len(ascii_list)) % len(ascii_list)] for i in range(len(ascii_list))]

def xor_base(ascii_list: List[int], key: List[int], base: int, start_idx: int, end_idx: int) -> List[int]:
    """
    Applies a sequence of XOR operations on a list of ASCII values using a base value and a key.

    Args:
        ascii_list: The list of ASCII values to transform.
        key: The list of integers to XOR with each value in `ft`.
        base: The initial value to XOR with the first element in `ft`.
        start_idx: The index of the key to start using for XOR operations.
        end_idx: The index of the key to stop using for XOR operations.

    Returns:
        A new list of transformed ASCII values.
    """
    key_len = len(key[start_idx:end_idx])
    final = []
    for i in range(len(ascii_list)):
        xor = ascii_list[i] ^ key[start_idx:end_idx][i % key_len] ^ base
        final.append(xor)
        base = xor
    return final

def unxor_base(ascii_list: List[int], key: List[int], base: int, start_idx: int, end_idx: int) -> List[int]:
    """
    Reverses the sequence of XOR operations on a list of ASCII values using a base value and a key.

    Args:
        ascii_list: The list of transformed ASCII values to transform back to the original order.
        key: The list of integers used to XOR with each value in `ft`.
        base: The initial value used to XOR with the first element in `ft`.
        start_idx: The index of the key to start using for XOR operations.
        end_idx: The index of the key to stop using for XOR operations.
    
    Returns:
        A new list of ASCII values in the original order.
    """
    key_len = len(key[start_idx:end_idx])
    final = []
    prev_xor = base
    for i in range(len(ascii_list)):
        xor = ascii_list[i] ^ key[start_idx:end_idx][i % key_len] ^ prev_xor
        final.append(xor)
        prev_xor = ascii_list[i]
    return final

def xor_add(ascii_list: List[int], key: List[int], start_idx: int, end_idx: int) -> List[int]:
    """
    Applies a sequence of addition and XOR operations on a list of ASCII values using a key.

    Args:
        ascii_list: The list of ASCII values to transform.
        key: The list of integers to use for addition and XOR operations.
        start_idx: The index of the key to start using for operations.
        end_idx: The index of the key to stop using for operations.

    Returns:
        A new list of transformed ASCII values.
    """
    ft_len = len(ascii_list)
    key_len = len(key[start_idx:end_idx])
    transformed_values = []
    for i in range(ft_len):
        value = ascii_list[i]
        key_value = key[start_idx:end_idx][i % key_len] & 127
        transformed_values.append((value + key_value) % 256 ^ 128)
    return transformed_values

def xor_unadd(ascii_list: List[int], key: List[int], start_idx: int, end_idx: int) -> List[int]:
    """
    Reverses the sequence of addition and XOR operations on a list of ASCII values using a key.

    Args:
        ascii_list: The list of transformed ASCII values to transform back to the original order.
        key: The list of integers used for addition and XOR operations.
        start_idx: The index of the key to start using for operations.
        end_idx: The index of the key to stop using for operations.

    Returns:
        A new list of ASCII values in the original order.
    """
    ft_len = len(ascii_list)
    key_len = len(key[start_idx:end_idx])
    original_values = []
    for i in range(ft_len):
        value = ascii_list[i]
        key_value = key[start_idx:end_idx][i % key_len] & 127
        original_values.append((value ^ 128) - key_value % 256)
    return original_values

def interleave_key(ascii_list: List[int], key: List[int], start_idx: int, end_idx: int) -> List[int]:
    """
    Interleaves a list of ASCII values with corresponding key values.

    Args:
        ascii_list: The list of ASCII values to interleave.
        key: The list of integers to interleave with `ascii_list`.
        start_idx: The index of the key to start using for interleaving.
        end_idx: The index of the key to stop using for interleaving.

    Returns:
        A new list of interleaved ASCII values and key values.
    """
    key_len = len(key[start_idx:end_idx])
    interleaved_list = []
    for i, value in enumerate(ascii_list):
        interleaved_list.append(value)
        interleaved_list.append(key[start_idx:end_idx][i % key_len])
    return interleaved_list

def deinterleave_key(ascii_list: List[int], key: List[int], start_idx: int, end_idx: int) -> List[int]:
    """
    Deinterleaves a list of ASCII values and key values.

    Args:
        ascii_list: The list of interleaved ASCII values and key values to transform back to the original order.
        key: The list of integers used to interleave with `ascii_list`.
        start_idx: The index of the key to start using for deinterleaving.
        end_idx: The index of the key to stop using for deinterleaving.

    Returns:
        A new list of ASCII values in the original order.
    """
    _ = len(key[start_idx:end_idx])
    original_list = []
    for i in range(0, len(ascii_list), 2):
        original_list.append(ascii_list[i])
    return original_list

def reverse(ascii_list: List[int]) -> List[int]:
    """
    Reverses a list of ASCII values.

    Args:
        ascii_list: The list of ASCII values to reverse.

    Returns:
        A new list of ASCII values in the reverse order.
    """
    return ascii_list[::-1]

OPPOSITE_ENCRYPTION_FUNCTIONS = {
    'swap': swap_back,
    'swap_back': swap,
    'xor_shift': xor_unshift,
    'xor_unshift': xor_shift,
    'interleave': deinterleave,
    'deinterleave': interleave,
    'rotate': unrotate,
    'unrotate': rotate,
    'xor_base': unxor_base,
    'unxor_base': xor_base,
    'xor_add': xor_unadd,
    'xor_unadd': xor_add,
    'interleave_key': deinterleave_key,
    'deinterleave_key': interleave_key,
    'reverse': reverse,
}

def clean_input(string: str) -> str:
    """
    Cleans a string to be used as a JSON string.

    Args:
        string: The string to clean.

    Returns:
        The cleaned string.
    """
    # Convert unicode character to escaped unicode
    def escape_unicode(uu):
        return "\\u" + ("0000" + hex(ord(uu))[2:])[-4:]

    # Regular expression to match Unicode characters
    unicode_regex = r'[\u007F-\uFFFF]'

    # Replace Unicode characters with escaped Unicode
    return sub(unicode_regex, lambda m: escape_unicode(m.group(0)), dumps(string, separators=(',', ':')))

def revert_clean_input(cleaned_string: str) -> str:
    """
    Revert a cleaned string (with escaped Unicode characters) back to the original string.

    Args:
        cleaned_string: The cleaned string with escaped Unicode characters.

    Returns:
        The original string.
    """
    # Regular expression to match escaped Unicode characters
    escaped_unicode_regex = r'\\u[0-9a-fA-F]{4}'

    # Replace escaped Unicode characters with actual Unicode characters
    unescaped_string = sub(escaped_unicode_regex, lambda m: chr(int(m.group(0)[2:], 16)), cleaned_string)

    # Load the unescaped string as a JSON object to get the original string
    return loads(unescaped_string)
