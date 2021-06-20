# infix_expression_parser

Infix expression calculator written in python

- It has a expression validator (not sure if it is 100% correct)
- It accepts expressions like this: (((8 + 9) * 7) + 2) / 2

##  Algorithm:
There's a function that replaces all the content inside parentheses with variables and stores them into a dictionary.
(((8 + 9) * 7) + 2) / 2 -> ((a * 7) + 2) / 2 -> (b + 2) / 2 -> c / 2 , where c contains (b + 2), which b contains (a * 7) and a contains (8 + 9). 
The algorithm to calculate the expressions is trivial.

## Run it as:
```
python3 main.py
```
