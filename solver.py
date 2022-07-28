import time
import cProfile
import sys
sys.setrecursionlimit(10000)

def split_exp(exp):
  return exp.replace('+', ' + ').replace('*', ' * ').replace('/', ' / ').split()

def decompose(exp):
  if '-' in exp:
    exp = exp.replace('-', '+-')
    if exp[0] == '+':
      exp = exp[1:]
  
  exp = split_exp(exp)
  return exp

def perform_op(exp, idx_1, idx_2, op):
  match op:
    case '+': 
      exp[idx_1] = float(exp[idx_1]) + float(exp[idx_2])
    case '*':
      exp[idx_1] = float(exp[idx_1]) * float(exp[idx_2])
    case '/':
      exp[idx_1] = float(exp[idx_1]) / float(exp[idx_2])

  exp.pop(idx_1+1)
  exp.pop(idx_1+1)

  return exp

def ret_index(lst, val):
  try:
    return lst.index(val)
  except ValueError:
    return -1

def solve(exp):
  exp = decompose(exp)
  return _solve(exp)

def old_solve(exp):
  exp = decompose(exp)
  return _solve_(exp)

#@profile
def _solve_(exp):
  if '+' not in exp and '*' not in exp and '/' not in exp:
    assert len(exp) == 1, 'Invalid expression:  %s' % exp
    return float(exp[0])

  if '*' in exp or '/' in exp:
    op_idx_times = ret_index(exp, '*')
    op_idx_div = ret_index(exp, '/')
    if op_idx_div == -1 or (op_idx_times < op_idx_div and op_idx_times != -1):
      exp = perform_op(exp, op_idx_times-1, op_idx_times+1, exp[op_idx_times])
    else:
      exp = perform_op(exp, op_idx_div-1, op_idx_div+1, exp[op_idx_div])
  else:
    exp = perform_op(exp, ret_index(exp, '+')-1, ret_index(exp, '+')+1, '+')

  return _solve_(exp)

def _solve(exp):

  if len(exp) == 1:
    return float(exp[0])
  if len(exp) == 3:
    return float(perform_op(exp, 0, 2, exp[1])[0])
  
  for i in range(len(exp)-4):
    if exp[i] in ['+', '*', '/']:
      continue
    curr_op = exp[i+1]
    next_op = exp[i+3]
    if next_op in ['*', '/'] and curr_op not in ['*', '/']:
      exp = perform_op(exp, i+2, i+4, next_op)
    else:
      exp = perform_op(exp, i, i+2, curr_op)
    break
    

  return _solve(exp)

      
from exp_gen import ExpGen
from not_mine import evaluate
from not_mine2 import Solution

expressions = ExpGen(max_terms=100, parenthesis_prob=0, max_number=100, seed=420).generate(10000)

print('Old Mine:')
start = time.time()
for pair in expressions:
  solved = old_solve(pair[0])
  if round(solved, 3) != round(pair[1], 3):
    print("Expression: %s\nOutput: %s\nExpected: %s" % (pair[0], solved, pair[1]))
print("Time: %s" % (time.time() - start))

print('Mine:')
start = time.time()
for pair in expressions:
  solved = solve(pair[0])
  if round(solved, 3) != round(pair[1], 3):
    print("Expression: %s\nOutput: %s\nExpected: %s" % (pair[0], solved, pair[1]))
print("Time: %s" % (time.time() - start))

print('-------------------------------')

print('Not Mine:')
start = time.time()
for pair in expressions:
  solved = evaluate(pair[0])
  if round(solved, 3) != round(pair[1], 3):
    print("Expression: %s\nOutput: %s\nExpected: %s" % (pair[0], solved, pair[1]))
print("Time: %s" % (time.time() - start))

ob = Solution()
print('Not Mine2:')
start = time.time()
for pair in expressions:
  solved = ob.solve(pair[0])
print("Time: %s" % (time.time() - start))

print('Eval:')
start = time.time()
for pair in expressions:
  solved = eval(pair[0])
  if round(solved, 3) != round(pair[1], 3):
    print("Expression: %s\nOutput: %s\nExpected: %s" % (pair[0], solved, pair[1]))
print("Time: %s" % (time.time() - start))