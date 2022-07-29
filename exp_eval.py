class ExpEval:
  def __init__(self):
    self.reset_var()
    self.operators = ['+', '-', '*', '/', '**']

  @property
  def _var(self):
    self.var_number += 1
    return 'A' + str(self.var_number)
  
  def reset_var(self):
    self.var_number = 0
    self.V = {}
  
  def _preprocessing(self, exp):
    return exp.replace(' ', '').replace('**', '^')
  
  def _postprocessing(self, exp):
    return exp.replace('^', '**')
  
  def _is_single_var(self, x):
    try:
      x = int(x)
      return False
    except ValueError:
      if x in self.V:
        return True
      return False 

  def _split(self, exp):
    assert '(' not in exp, 'Expression contains parenthesis'

    # split by multi delimiters (operators)
    for op in self.operators:
      exp = exp.replace(op, ' ' + op + ' ')
    splited = exp.split()
    splited = [x for x in splited if x not in self.operators and self._is_single_var(x)]
    return splited

  def _split_exp(self, exp):
    assert '(' not in exp, 'Expression contains parenthesis'

    # split by multi delimiters (operators)
    for op in self.operators:
      exp = exp.replace(op, ' ' + op + ' ')
    splited = exp.split()
    splited = [x for x in splited]
    return splited



  def _get_parenthesis_indexes(self, exp):
    """
    Returns the index of the first parenthesis occurrence in the expression.
    ex: ((2**3))+7*(3+4) -> (0, 7)
    """
    assert '(' in exp, 'Parenthesis not found in expression'

    indexes = []
    stack = []
    for i, char in enumerate(exp):
      if char == '(':
        stack.append(1)
        if len(indexes) == 0:
          indexes.append(i)
      elif char == ')':
        stack.pop()
      if len(stack) == 0 and len(indexes) == 1:
        indexes.append(i)
        break
    
    return indexes


  def _replace_parenthesis_rec(self, exp):
    """
    Replaces all the content recursivelly in the expression.
    """

    if '(' not in exp:
      return exp
    
    exp = self._replace_parenthesis(exp)
    splited = self._split(exp)
    for var in splited:
      self.V[var] = self._replace_parenthesis_rec(self.V[var])
    
    return exp


  def _replace_parenthesis(self, exp):
    """
    Takes an expression and replaces all the parenthesis with a letter.
    ex: (2**3)+7*(3+4) -> (A1+7*A2), where A1 = (2**3) and A2 = (3+4)
    ex: 9 -> 9
    """

    while '(' in exp:
      indexes = self._get_parenthesis_indexes(exp)
      # save parenthesis content 
      var = self._var
      self.V[var] = exp[indexes[0]+1:indexes[1]]
      # replace with content with a letter
      exp = exp[:indexes[0]] + var + exp[indexes[1]+1:]

    return exp
  
  def _solve_vars(self, exp):
    splited_exp = self._split_exp(exp)

    for i,x in enumerate(splited_exp):
      if x not in self.operators and self._is_single_var(x):
        splited_exp[i] = self._solve_vars(self.V[x])
    
    a = "".join(map(str, splited_exp))

    return self._expression_tree(a)
    

  def _expression_tree(self, exp):
    return self.new_solve(exp)

  """
  def ultra_split(self, exp):
    exp = exp.replace('*-', '&').replace('/-', '$').replace('--', '+')
    exp = exp.replace('-', '+-').replace('&', '*-').replace('$', '/-')
    if exp[0] == '+':
      return exp[1:].split('+')
    return exp.split('+')
  """

  def ultra_split(self, exp):
    exp = exp.replace('*-', '&').replace('/-', '$').replace('--', '+')
    exp = exp.replace('e-', '#').replace('e+', '@').replace('-', '+-').replace('+', ' + ')
    exp = exp.replace('#', 'e-').replace('@', 'e+').replace('&', '*-').replace('$', '/-')
    if exp[0] == '+':
      return exp[1:].split('+')
    return list(filter(None, exp.split(' + ')))

  def is_number(self, num):
    try:
      float(num)
      return True
    except ValueError:
      return False

  #@profile
  def new_solve(self, exp):
    exp = self.ultra_split(exp)
    #print(exp)
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




  def evaluate(self, exp):
    exp = self._preprocessing(exp)
    exp = self._replace_parenthesis_rec(exp)
    print(exp)
    res = self._solve_vars(exp)
    #res = self._expression_tree(exp)
    print(res)
    exit(0)
    res = self._expression_tree(exp)
    exp = self._postprocessing(exp)
    print('Expression: %s' % exp)
    print(self.V)
    self.reset_var()
    return res
  
  def new_evaluate(self, exp):
    if '('  not in exp:
      res = self.new_solve(exp) 
      return str(res)
    indexes = self._get_parenthesis_indexes(exp)
    exp = list(exp)
    exp[indexes[1]] =  self.new_evaluate("".join(exp[indexes[0]+1:indexes[1]]))
    del exp[indexes[0]:indexes[1]]

    return self.new_evaluate("".join(exp))


if __name__ == '__main__':
  exp = "6/30-(82*(88*82*((28-43-(((34)-77*47+(31))+15)/40)*95-72+((93))+95-(53))*94)*(68+(21-((94*(58))))*28)-((41))-(9)/66*((59))/((18)))+(97)+5/(32)-55"
  myeval = ExpEval()
  print(myeval.new_evaluate(exp), eval(exp))
  