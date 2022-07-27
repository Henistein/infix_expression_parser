"""
class ExpEval:
  def __init__(self):
    self.reset_var()
    self.operators = ['+', '-', '*', '/', '^']

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
  
  def _is_var(self, x):
    try:
      x = int(x)
      return False
    except ValueError:
      return True

  def _split(self, exp):
    assert '(' not in exp, 'Expression contains parenthesis'

    # split by multi delimiters (operators)
    for op in self.operators:
      exp = exp.replace(op, ' ' + op + ' ')
    splited = exp.split()
    splited = [x for x in splited if x not in self.operators and self._is_var(x)]
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
  
  def _expression_tree(self, exp):
    if '+' in exp: 
      splited = exp.split('+')
      return self._expression_tree(splited[0]) + self._expression_tree(splited[1])
    elif '-' in exp:
      splited = exp.split('-')
      return self._expression_tree(splited[0]) - self._expression_tree(splited[1])
    elif '*' in exp:
      splited = exp.split('*')
      return self._expression_tree(splited[0]) * self._expression_tree(splited[1])
    elif '/' in exp:
      splited = exp.split('/')
      return self._expression_tree(splited[0]) / self._expression_tree(splited[1])
    elif '^' in exp:
      splited = exp.split('^')
      return self._expression_tree(splited[0]) ** self._expression_tree(splited[1])
    else:
      if self._is_var(exp):
        return self._expression_tree(self.V[exp])
      return int(exp)




  def evaluate(self, exp):
    e = exp
    exp = self._preprocessing(exp)
    exp = self._replace_parenthesis_rec(exp)
    res = self._expression_tree(exp)
    exp = self._postprocessing(exp)
    self.reset_var()
    return res
"""
class ExpEval:
  def __init__(self):
    self.reset_var()
    self.operators = ['+', '-', '*', '/', '^']

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
  
  def _is_var(self, x):
    try:
      x = int(x)
      return False
    except ValueError:
      return True

  def _split(self, exp):
    assert '(' not in exp, 'Expression contains parenthesis'

    # split by multi delimiters (operators)
    for op in self.operators:
      exp = exp.replace(op, ' ' + op + ' ')
    splited = exp.split()
    splited = [x for x in splited if x not in self.operators and self._is_var(x)]
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
  
  def _expression_tree(self, exp):
    if '+' in exp: 
      splited = exp.split('+')
      return self._expression_tree(splited[0]) + self._expression_tree(splited[1])
    elif '-' in exp:
      splited = exp.split('-')
      return self._expression_tree(splited[0]) - self._expression_tree(splited[1])
    elif '*' in exp:
      splited = exp.split('*')
      return self._expression_tree(splited[0]) * self._expression_tree(splited[1])
    elif '/' in exp:
      splited = exp.split('/')
      return self._expression_tree(splited[0]) / self._expression_tree(splited[1])
    elif '^' in exp:
      splited = exp.split('^')
      return self._expression_tree(splited[0]) ** self._expression_tree(splited[1])
    else:
      if self._is_var(exp):
        return self._expression_tree(self.V[exp])
      return int(exp)




  def evaluate(self, exp):
    e = exp
    exp = self._preprocessing(exp)
    exp = self._replace_parenthesis_rec(exp)
    res = self._expression_tree(exp)
    exp = self._postprocessing(exp)
    self.reset_var()
    return res