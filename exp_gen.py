import numpy.random as random
from tqdm import trange

# TODO: Fix recursion issues
# TODO: Fix overflow issues
# TODO: Fix cast issues

class ExpGen:
  # generate an expression X
  # generate number of terms
  # example: 3 terms X -> A1_A2_A3 
  # for each term generate a number or an expression
  # example: A1 -> 1 or A1 -> (X)
  # for each _ choose a random operator (+, -, *, /, ^)
  def __init__(self, max_terms=10, max_number=10):
    self.operators = ['+', '-', '*', '/', '**']
    self.max_terms = max_terms + 1
    self.max_terms_back = max_terms + 1
    self.max_number = max_number
  
  def _generate(self):
    # probability of 0.70 to decrease the number of terms
    if random.random() < 0.7:
      self.max_terms -= 1
      if self.max_terms < 2:
        self.max_terms = 2
      
    n_terms = random.randint(1, self.max_terms)
    terms = '_'.join([str(random.choice([random.randint(1, self.max_number), 'X'], p=[0.6, 0.4])) for _ in range(n_terms)])

    # swap all the _ with random operators
    terms = [random.choice(self.operators, p=[0.24, 0.24, 0.24, 0.24, 0.04]) if elem == '_' else elem for elem in terms]

    if 'X' not in terms:
      return ''.join(terms)
    else:
      # list of all indexes of X
      indexes = [i for i, elem in enumerate(terms) if elem == 'X']
      for i in indexes:
        # replace X with a random operator
        terms[i] = '(' + self._generate() + ')'
      return ''.join(terms)
  
  def generate(self, n_expressions=1):
    expressions = []
    for _ in trange(n_expressions):
      tries = 0
      self.max_terms = self.max_terms_back
      while True:
        if tries == 100:
          print('100 tries failed, returning (0, 0)...')
          return (0, 0)
        try:
          exp = self._generate()
          res = eval(exp)
          break
        except (ZeroDivisionError, OverflowError):
          tries += 1
          exp = self._generate()
      expressions.append((exp, res))
    return expressions
      
  

if __name__ == '__main__':
  print(ExpGen().generate(1000))