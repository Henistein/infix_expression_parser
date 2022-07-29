from ast import Expression
import time
import sys

sys.setrecursionlimit(1000000)

def ultra_split(exp):
  exp = exp.replace('+', ' + ')
  #exp = exp.replace('*-', '&').replace('/-', '$').replace('--', '+')
  #exp = exp.replace('-', '+-').replace('&', '*-').replace('$', '/-')
  if exp[0] == '+':
    return exp[1:].split('+')
  #return exp.split('+')
  return exp.split(' + ')


def is_number(num):
  try:
    float(num)
    return True
  except ValueError:
    return False

#@profile
def new_solve(exp):
  exp = ultra_split(exp)
  res = 0
  res2 = None
  for x in exp:
    if is_number(x):
      res += float(x)
    else:
      splited = x.replace('*', ' * ').replace('/', ' / ').split()
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



      
from exp_gen import ExpGen, load 
from not_mine import evaluate
from not_mine2 import Solution


exp = '46+-14.708333333333334+99.0'
print(new_solve(exp), eval(exp))
exit(0)
expressions = load(False)
#expressions = ExpGen(max_terms=2, parenthesis_prob=0, seed=420).generate(10000)

print('New Mine:')
start = time.time()
for pair in expressions:
  solved = new_solve(pair[0])
  if round(solved, 3) != round(pair[1], 3):
    print("Expression: %s\nOutput: %s\nExpected: %s" % (pair[0], solved, pair[1]))
print("Time: %s" % (time.time() - start))

print('-------------------------------')

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