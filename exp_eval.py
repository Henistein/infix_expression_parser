from clibs.expressions import get_parenthesis_index

class ExpEval:
  def __init__(self):
    self.operators = ['+', '-', '*', '/', '**']

  #@profile
  def _get_parenthesis_indexes(self, exp):
    """
    Returns the index of the first parenthesis occurrence in the expression.
    ex: ((2**3))+7*(3+4) -> (0, 7)
    """

    indexes = []
    count = 0
    for i, char in enumerate(exp):
      if char == '(':
        count += 1
        if len(indexes) == 0:
          indexes.append(i)
      elif char == ')':
        count -= 1
      if count == 0 and len(indexes) == 1:
        indexes.append(i)
        break
    
    return indexes



  #@profile
  def ultra_split(self, exp):
    exp = exp.replace('*-', '&').replace('/-', '$').replace('--', '+')
    exp = exp.replace('e-', '#').replace('e+', '@').replace('-', '+-').replace('+', ' + ')
    exp = exp.replace('#', 'e-').replace('@', 'e+').replace('&', '*-').replace('$', '/-')
    if exp[0] == '+':
      return exp[1:].split('+')
    return list(filter(None, exp.split(' + ')))

  #@profile
  """
  def ultra_split(self, exp):
    exp = exp.split('+')
    
    if exp[0] == '+':
      return exp[1:].split('+')
    return list(filter(None, exp.split(' + ')))

  """
  def is_number(self, num):
    return (False if '*' in num or '/' in num else True)


  #@profile
  def new_solve(self, exp):
    exp = self.ultra_split(exp)
    res = 0
    res2 = None
    for x in exp:
      if self.is_number(x):
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


  #@profile
  def new_evaluate(self, exp):
    if '('  not in exp:
      res = self.new_solve(exp) 
      return str(res)

    #indexes = self._get_parenthesis_indexes(exp)
    indexes = get_parenthesis_index(exp)
    exp = list(exp)
    exp[indexes[1]] =  self.new_evaluate("".join(exp[indexes[0]+1:indexes[1]]))
    del exp[indexes[0]:indexes[1]]

    return self.new_evaluate("".join(exp))


import time
from exp_gen import ExpGen,load

if __name__ == '__main__':
  expressions = load(True)
  #expressions = ExpGen(max_terms=10, parenthesis_prob=0.5, max_number=1000).generate(100)

  myeval = ExpEval()
  print('New Mine:')
  start = time.time()
  for pair in expressions:
    #print(pair)
    solved = float(myeval.new_evaluate(pair[0]))
    if round(solved, 3) != round(pair[1], 3):
      print("Expression: %s\nOutput: %s\nExpected: %s" % (pair[0], solved, pair[1]))
  print("Time: %s" % (time.time() - start))