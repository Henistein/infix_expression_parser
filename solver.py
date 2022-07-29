import time
import cProfile
import sys
import queue

sys.setrecursionlimit(1000000)

def split_exp(exp):
  return exp.replace('+', ' + ').replace('*', ' * ').replace('/', ' / ').split()

def decompose(exp):
  if '-' in exp:
    exp = exp.replace('-', '+-')
    if exp[0] == '+':
      exp = exp[1:]
  
  exp = split_exp(exp)
  return exp

#@profile
def perform_op(exp, idx_1, idx_2, op):
  match op:
    case '+': 
      exp[idx_2] = float(exp[idx_1]) + float(exp[idx_2])
    case '*':
      exp[idx_2] = float(exp[idx_1]) * float(exp[idx_2])
    case '/':
      exp[idx_2] = float(exp[idx_1]) / float(exp[idx_2])


  del exp[0:idx_2]

def solve(exp):
  exp = decompose(exp)
  return _solve(exp)

def ultra_split(exp):
  # "1+1+2*3/4+-5" -> "1+1", "2*3/4", "-5" -> [["1", "+", "1"],["2", "*", "3", "/", "4"], ["-5"]]
  if '-' in exp:
    exp = exp.replace('-', '+-')
    if exp[0] == '+':
      exp = exp[1:]
  return exp.split('+')

def little_split(exp):
  return exp.replace('*', ' * ').replace('/', ' / ').split()

def is_number(num):
  try:
    float(num)
    return True
  except ValueError:
    return False

def new_solve(exp):
  exp = ultra_split(exp)

  res = 0
  res2 = None
  for x in exp:
    if is_number(x):
      res += float(x)
    else:
      splited = little_split(x)
      for i in range(1, len(splited), 2):
        match splited[i]:
          case '*':
            if res2 is None:
              res2 = float(splited[i-1]) * float(splited[i+1])
            else:
              res2 *= float(splited[i+1])
          case '/':
            if res2 is None:
              res2 = float(splited[i-1]) / float(splited[i+1])
            else:
              res2 /= float(splited[i+1])
      res += res2
      res2 = None
  return res


def _solve(exp):


  ans = 0
  while True:
    if len(exp) == 1:
      return ans + float(exp[0])
    if len(exp) == 3:
      perform_op(exp, 0, 2, exp[1])
      return ans + float(exp[0])
    
    curr_op = exp[1]
    next_op = exp[3]
    if next_op in ['*', '/'] and curr_op not in ['*', '/']:
      ans += float(exp[0])
      perform_op(exp, 2, 4, next_op)
    else:
      perform_op(exp, 0, 2, curr_op)

      
from exp_gen import ExpGen
from not_mine import evaluate
from not_mine2 import Solution

#print(new_solve('26/12/94-54/20'), eval('26/12/94-54/20'))
#exit(0)
expressions = ExpGen(max_terms=100000, parenthesis_prob=0, max_number=100, seed=420).generate(10)

print('New Mine:')
start = time.time()
for pair in expressions:
  solved = new_solve(pair[0])
  if round(solved, 3) != round(pair[1], 3):
    print("Expression: %s\nOutput: %s\nExpected: %s" % (pair[0], solved, pair[1]))
print("Time: %s" % (time.time() - start))

print('Mine:')
start = time.time()
for pair in expressions:
  solved = solve(pair[0])
  """
  if round(solved, 3) != round(pair[1], 3):
    print("Expression: %s\nOutput: %s\nExpected: %s" % (pair[0], solved, pair[1]))
  """
print("Time: %s" % (time.time() - start))

print('-------------------------------')
ob = Solution()
print('Not Mine:')
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