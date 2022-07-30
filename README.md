# Infix expression parser

Infix expression calculator written in python

- It accepts expressions like this: (((8 + 9) * 7) + 2) / 2
- We wrote some methods in c so it can be super fast
- We present a Expression generator that is useful to generate expressions


## Try Expression Evaluation as:
```python
from exp_eval import ExpEval

myeval = ExpEval()
print(myeval.new_evaluate("(((8+9)*7)+2)/2")) # 60.5
```

## Try Expression Generator as:
```python
from exp_gen import ExpGen

mygen = ExpGen()
expressions = ExpGen(max_terms=10, parenthesis_prob=0.5, max_number=100000).generate(10)
```


## TODO:
- Refactor C and Python Code
- Further improve performance (if possible)
