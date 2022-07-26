import random
import sys
sys.setrecursionlimit(10000)

class ExpGen:
  # generate an expression X
  # generate number of terms
  # example: 3 terms X -> A1_A2_A3 
  # for each term generate a number or an expression
  # example: A1 -> 1 or A1 -> (X)
  # for each _ choose a random operator (+, -, *, /, ^)
  def __init__(self, max_terms=3, max_number=10):
    self.operators = ['+', '-', '*', '/', '**']
    self.max_terms = max_terms
    self.max_number = max_number
  
  def generate(self):
    n_terms = random.randint(1, self.max_terms)
    terms = '_'.join([str(random.choice([random.randint(0, self.max_number), 'X'])) for _ in range(n_terms)])

    # swap all the _ with random operators
    terms = [random.choice(self.operators) if elem == '_' else elem for elem in terms]

    if 'X' not in terms:
      return ''.join(terms)
    else:
      # list of all indexes of X
      indexes = [i for i, elem in enumerate(terms) if elem == 'X']
      for i in indexes:
        # replace X with a random operator
        terms[i] = '(' + self.generate() + ')'
      return ''.join(terms)
      
  

if __name__ == '__main__':
  for i in range(1000):
    print(ExpGen().generate())