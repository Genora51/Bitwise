# Documentation

Bitwise is a surprisingly simple language in terms of format. But that's about where it ends in terms of simplicity.

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

  *Bear in mind that this does not always return 1, because binary numbers in Bitwise are not automatically stripped of leading zeros.*
- `'` : This is largely used in loops to reference a counter.
  `'n` refers to digit `"` of `n`, where `"` is the loop counter variable.
  This is equivalent to the expression `n@"`

## Binary Operators (pun intended)

Binary operators take 2 expressions as input: a left side and a right side.

- `+` : The `OR` operator. E.g. `1100 + 1010` = `1110`
- `&` : The `AND` operator. E.g. `1100 & 1010` = `1000`
- `^` : The `XOR` operator. E.g. `1100 ^ 1010` = `0110`

Each of these has an opposite, equivalent to applying the `!` operator to the resultant number:

- `!+` : The `NOR` operator. E.g. `1100 !+ 1010` = `0001`
- `!&` : The `NAND` operator. E.g. `1100 !& 1010` = `0111`
- `!^`: The `NXOR` operator. E.g. `1100 !^ 1010` = `1001`

Other operators:

- `>>` : The right shift operator.
  `a >> b` is equivalent to a/2<sup>b</sup> (rounded down) e.g. `10110 >> 11` = `10`
- `<<` : The left shift operator.
  `a << b` is equivalent to a\*2<sup>b</sup> e.g. `101 << 11` = `101000`
- `.` : The concatenation operator e.g. `101 . 111` = `101111`
- `@` : The position operator.
  `a@b` returns the digit of a at index b, starting from the units digit.
  E.g. `100110 @ 11` = `1` (the third digit from the right)
- `_` : The max operator.
  Returns the maximum of its operands e.g. `11_1001` = `1001`

## Input/Output

Input/output statements take a very similar format to each other.

### Input
Input statements take the form `I> setVar`, where `setVar` is the variable to be set.

There are 4 input commands:
- `>`: Takes in a binary number e.g. `1001`
- `I>`: Takes in a decimal integer and converts it to binary e.g. `6` &rarr; `110`
- `H>`: Takes in a hexadecimal integer and converts it to binary e.g. `F3` &rarr; `11110011`
- `S>`: Takes in a string and converts it to its ASCII binary representation e.g. `a` &rarr; `01100001`

### Output
Output statements take the form `I< EXPR`, where `EXPR` is any valid expression.

Each input command in Bitwise has a corresponding output command:
- `<`: Ouputs in binary e.g. `101`
- `I<`: Outputs in decimal e.g. `110` &rarr; `6`
- `H<`: Outputs in hexadecimal e.g. `1011` &rarr; `B`
- `S<`: Outputs as ASCII e.g. `01100001` &rarr; `a`

## Control Structures
Control Structures in Bitwise are used for code that should run multiple times, or conditionally.
All control structures take the following form (indentation and spacing here are only for readability):

    CON EXP
      STATEMENT 1
      STATEMENT 2
      ETC.
    ;
Here, `CON` represents the control identifier e.g. `?`.
`EXP` should be replaced with some expression e.g. the check condition of an if-statement.
In between the expression and the closing semicolon can be placed a series of commands,
run according to the control structure used.

In Bitwise, there are 3 control structures: `?`, `-`, and `~`.

### If-Statements
The `?` character is used to denote an if-statement.
The if-statement checks if the passed expression evaluates to non-zero,
and if this is true, runs the commands.

For example, this code would check if the variable `a` is non-zero, and if so,
prints out the hexadecimal value of `a` OR `b` (b is another variable).

    ?a
      H< a+b
    ;

### Digit Loops
Digit loops iterate for each digit of the passed expression.

There are two digit loops in Bitwise.

#### Right-digit loop
This loop, signified by the `-` character, iterates from the right-hand digit.
The counter variable `"` starts at 0 and increments with each iteration.
This can be used to reference back to the original expression with the `'` command.

For example, this program iterates over the number `1011` and prints each digit, starting from the units column.

    a = 1011
    -a
      < 'a
    ;
This program would output:

    1
    1
    0
    1

#### Left-digit loop
This loop, represented by the `~` character,
is the reverse of the right-digit loop, as it starts from the left.
The counter variable starts at the length of the passed expression, and ends at 0.
It decrements with each iteration.

The program below iterates over the number `1011` and prints each digit in order.

    a = 1011
    ~a
      < 'a
    ;

This program would output:

    1
    0
    1
    1
