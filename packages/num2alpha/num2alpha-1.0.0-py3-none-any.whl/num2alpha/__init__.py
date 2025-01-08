# ---------------
# Created by Samarthya Lykamanuella.
# GPL-3.0-licensed
# ---------------
# 
# This program converts a non-zero positive integer into its mapping
# in the alphabetical form; and vice-versa

# The variables 'd', 'e', and 'f' in this script are thought to be the
# "variable conventions" used as a catch-all for a function's argument

import math

# ----------------------- FUNCTION DECLARATION ----------------------- #

# Should we echo debuggings?
is_echo = False

alpha_list = [
    'a','b','c','d','e','f','g','h','i','j','k','l','m',
    'n','o','p','q','r','s','t','u','v','w','x','y','z'
]

def find_alpha(d):
    """
    This function converts a positive integer of range 1-26 into its
    respective alphabet correspondence.
    
    Accepts only number from 1 to 26.
    
    Returns a string.
    """
    
    return alpha_list[d-1]

def find_number(d):
    """
    This function converts any letter-digit of alphabet into its
    non-zero positive integer representation in base-10.
    
    Accepts only singular characters from the set of [a-z][A-Z].
    
    Returns an integer.
    """
    
    # Fail-safe; in case user got the string input mad
    d = d.lower()
    
    return alpha_list.index(d) + 1  # --- array starts at zero!

# -------------------------------------------------------------------- #

def alpha_to_number(n):
    """
    Converts any alphabetical sequence into its corresponding
    numerical order in decimal (base-10).
    This function is case-insensitive, but only accepts [a-z][A-Z].
    
    Example uses:
    
    alpha_to_number('a')  # --- returns 1
    alpha_to_number('xY')  # --- returns 649
    alpha_to_number('heLLo')  # --- returns 3752127
    
    :return: An integer.
    """
    
    if type(n) != str:
        msg = 'alpha_to_number() can only do conversion on strings!'
        if is_echo:
            print(msg)
        raise TypeError(msg)
    
    elif not n.isalpha():
        msg = 'You can only input alphabets [a-z][A-Z] here!'
        if is_echo:
            print(msg)
        raise TypeError(msg)
    
    # The length of the string
    i = len(n)
    
    # Create the reversed array of the input letter-digit string
    a = list(n)
    a.reverse()
    
    # Where the sum of all letter-digits' value is stored
    j = 0
    
    # Let's loop 'em!
    # Each letter-digit ordinal carries different weight, exponential
    # in size; we start from the leftmost (i.e., the biggest ordinal)
    # All of this operation is just multiplication, exponential power,
    # and addition!
    while i > 0:
        # Find out what natural number does this letter-digit represent
        k = find_number(a[i-1])  # --- dammit, array starts at zero!
        
        # Then perform exponential power, multiplication, and finally
        # addition/sum into variable 'j'
        j += k * 26**(i-1)
        
        # Now let's decrement the iterator integer
        i -= 1
    
    # Finally, let us present the result of alphabet-to-integer parsing!
    if is_echo:
        print(f'''
    You asked for the base-10 integer representation of : {n}
    Here's what you got{' '*33}: {j}
        '''.strip()
        )
    
    return j

def number_to_alpha(n):
    """
    Converts any number form in decimal (base-10) into its
    corresponding alphabetical [a-z] sequence.
    This function only accepts integer.
    
    Example uses:
    
    number_to_alpha(1)  # --- returns 'a'
    number_to_alpha(23)  # --- returns 'w'
    number_to_alpha(27)  # --- returns 'aa'
    number_to_alpha(19203)  # --- returns 'abjo'
    
    :return: A string of the set [a-z].
    """
    
    if type(n) != int:
        msg = 'number_to_alpha() can only do conversion on integers!'
        if is_echo:
            print(msg)
        raise TypeError(msg)
    
    # The power factor of the base number "26"
    # Used to determine the number of letter digit
    # i.e., "lowest_upper_bound" = number of letter digit
    lowest_upper_bound = 1
    
    # Keep dividing the input number by 26 until
    # it gets smaller than 26, while adding the value of variable
    # "lowest_upper_bound" by one on each iteration
    i = int(n)
    while i > 26:
        i /= 26
        lowest_upper_bound += 1
    
    # Now, here's how we rudimentarily determine each letter-digit's
    # alphabet correspondence:
    # 1. Start from the leftmost/biggest letter-digit (e.g., "1" in
    #    "1402"; this sample number have three letter-digits)
    # 2. Floor-divide the whole number by 26 to the power of the
    #    leftmost letter-digit ordinal minus one (in this case of the
    #    four-digit number "1402", "2" is the letter-digit ordinal after
    #    substraction); The number that pops out after floor-division
    #    is the letter-digit's alphabet correspondence
    # 3. Shift to the next right letter-digit (e.g., "4" in "1402")
    # 4. Substract current whole number by value obtained from step 2
    #    (in case of the third letter-digit of "1402", substract
    #    by "1152" because 1402 - (2 * 26^2) is equal to 1152)
    # 5. Repeat steps 2-4 ad infinitum to the next right letter-digit
    
    # Let's create an array with the size corresponding to the value
    # of the variable "lowest_upper_bound"
    a = [None] * lowest_upper_bound
    
    # Start from the leftmost/biggest letter-digit order
    # Substracted value of current whole number will be stored in "i"
    # The letter-digit's alphabet correspondence value will be stored in
    # array "a" as a string, rather than raw integer
    i = int(n)
    j = int(lowest_upper_bound)
    while j > 0:
        # Floor-divide the current whole number ('i')
        # by 26 to the power of 'j-1'
        # Then find its alphabet correspondence and store into array "a"
        floor_division_result = math.floor(i / 26**(j-1))
        l = find_alpha(floor_division_result)
        a[j-1] = l  # --- array must start at zero!
        
        # Update the current whole number value as per substraction
        # with this letter-digit's geometric/exponential value
        # Then store this current whole number value into array "a"
        i -= floor_division_result * 26**(j-1)
        
        # Decrement the loop iterator variable
        j -= 1
    
    # Reverse the content of the digit-letter array "a" because
    # the biggest digit-letter ordinal comes up first
    a.reverse()
    
    # Finally, let us present the alphabetical representation!
    if is_echo:
        print(f'''
    You asked for the alphabetical representation of the number : {n}
    Here's your letter-digits{' '*35}: {''.join(a)}
        '''.strip()
        )
    
    return ''.join(a)
    
def autoconvert(chars):
    """
    :param chars: the string/integer to/from alpha from/to integer
    """
    
    # Let's store the user prompt in some nice string variable
    n = chars
    
    # Determining if the input argument is an integer or string
    # Then decides which code block to call upon
    
    if type(n) == str:
        # Let us parse letter-digit into natural number!
        return alpha_to_number(n)
        
    elif type(n) == int:
        # Let us convert from integer to letter-digit!
        return number_to_alpha(n)
    
    else:
        msg = 'You gotta be kidding! Pure strings xor integers only!'
        if is_echo:
            print(msg)
        raise TypeError(msg)
