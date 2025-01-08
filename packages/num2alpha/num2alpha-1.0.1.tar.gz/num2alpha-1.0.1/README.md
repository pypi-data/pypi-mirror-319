# num2alpha

## Description

This Python script converts any base-10 integer into its "alphabetical number" counterpart. For example, `1` is `a`, `26` is `z`, and `28` is `ab`. This alphabetical number order is exactly what you find in the column name of most modern spreadsheet apps.

This script can also decode an alphabetical number and return its integer order in base-10. For instance, the spreadsheet column `AXY` is counted as the `1325`-th column of the spreadsheed, and the string `helloworld` equals to `44580442473324`.

## Dependencies

This project depends on no third-party/external Python module. All modules required by `num2alpha` are already provided by the [Python Standard Library](https://docs.python.org/3/library/index.html).

## Installation

`num2alpha` is available for download through Python Package Index (PyPI). Run the following command in your operating system via the terminal:

```sh
python -m pip install num2alpha
```

## Usage

Import the `num2alpha` module as you would other modules.

```python
import num2alpha as n2a
```

Then you can convert alphabet sequences to their respective numerical order in base-10 using the function `alpha_to_number()`. This function is case-insensitive. Therefore, `alpha_to_number('abc')` will yield the same result as `alpha_to_number('ABC')` as well as `alpha_to_number('aBc')`.

```python
n2a.alpha_to_number('a')
# returns 1

n2a.alpha_to_number('z')
# returns 26

n2a.alpha_to_number('aa')
# returns 27

n2a.alpha_to_number('ab')
# returns 28

n2a.alpha_to_number('python')
# returns 201883748
```

To do the otherwise, i.e., converting numbers to their respective alphabet forms, use the function `number_to_alpha()`. Please only pass base-10 integers greater than 0 into it. If you pass a floating number or other non-integer types into it, `TypeError` will be raised.

The return string will be in the form of `[a-z]` (in lowercase).

```python
n2a.number_to_alpha(1)
# returns 'a'

n2a.number_to_alpha(2)
# returns 'b'

n2a.number_to_alpha(26)
# returns 'z'

n2a.number_to_alpha(27)
# returns 'aa'

n2a.number_to_alpha(2025)
# returns 'byw'

n2a.number_to_alpha(1234567890)
# returns 'cywoqvj'
```

If you are unsure about the type of data you are dealing with, you can use `autoconvert()` function to automatically determine whether the variable passed is a string of alphabetical characters or a base-10 integer. This function will then convert the passed argument accordingly.

```python
n2a.autoconvert(123)
# returns 'ds'

n2a.autoconvert('helloworld')
# returns 44580442473324
```
