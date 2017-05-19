# Documentation

Bitwise is a surprisingly simple language in terms of format.

## Whitespace
There are no whitespace restrictions of any kind (apart from comments, which end at a line break).

## Comments
Comments are single-line, starting anywhere and ending at the line break.
Comments are signified by the `/` symbol - the slash and everything after it are ignored by the interpreter.

Unfortunately, the only way to end a comment is a line break, so `/ comment / a & b` is all part of one comment.

## Literals

The only literals in bitwise are binary.
Binary literals take the form of a list of 1s and 0s e.g. `1010001010`.
However, no delimiters (e.g. spaces) between digits in a single literal are permitted.

## Variables and assignment

Variables are set by the statement `someVar = EXPRESSION`, where someVar is either:

1. A string of case-sensitive letters e.g. `myVariable`.
However, the underscore is an operator, so `my_var` is not a valid variable name.

2. The single character `"`. This is usually used as a control variable, but can be overwritten and accessed at will.

Variables are accessed simply by their identifiers, according to the rules laid out above.

## Unary Operators

There are only a few unary operators in Bitwise, but each serves an important function:

- `!` : The `NOT` operator. E.g. `!101` = `010`, or 2 in decimal;
- `#` : The right-strip operator.
Removes the first digit of a number e.g. `#1101` = `101`
- `$` : Returns the last digit of a number e.g. `$1110` = `0`
- `£` : Returns the first digit of a number e.g. `£100` = `1`
Bear in mind that this does not always return 1, because binary numbers in Bitwise are not automatically stripped of leading zeros.
- `'` : The `NOT` operator. E.g. `!101` = `010`, or 2 in decimal;
