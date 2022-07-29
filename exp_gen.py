import numpy.random as random
import multiprocessing
import time

from tqdm import trange

class ExpGen:
  # generate an expression X
  # generate number of terms
  # example: 3 terms X -> A1_A2_A3 
  # for each term generate a number or an expression
  # example: A1 -> 1 or A1 -> (X)
  # for each _ choose a random operator (+, -, *, /, ^)
  def __init__(self, max_terms=5, max_number=100, parenthesis_prob=0.4, seed=None):
    self.operators = ['+', '-', '*', '/']#, '**']
    self.p = [0.25, 0.25, 0.25, 0.25]#, 0.04]
    self.parenthesis_prob = parenthesis_prob
    self.max_terms = max_terms + 1
    self.max_terms_back = max_terms + 1
    self.max_number = max_number
    if seed is not None:
      random.seed(seed)
  
  def _eval(self, exp, queue):
    try:
      res = eval(exp)
      queue.put(res)
    except (ZeroDivisionError, OverflowError):
      queue.put(None)
  
  def _generate(self):
    # probability of 0.70 to decrease the number of terms
    if random.random() < 0.7:
      self.max_terms -= 1
      if self.max_terms < 2:
        self.max_terms = 2
      
    n_terms = random.randint(1, self.max_terms)
    terms = '_'.join([str(random.choice([random.randint(1, self.max_number), 'X'], p=[1-self.parenthesis_prob, self.parenthesis_prob])) for _ in range(n_terms)])

    # swap all the _ with random operators
    terms = [random.choice(self.operators, p=self.p) if elem == '_' else elem for elem in terms]

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

        exp = self._generate()
        # eval the expression, if it takes too long break
        queue = multiprocessing.Queue()
        p = multiprocessing.Process(target=self._eval, args=(exp,queue))
        p.start()
        start = time.time()
        while p.is_alive():
          if time.time() - start > 5:
            print('evaluation took too long...')
            p.terminate()
            p.join()
        # check if it was successful
        if not queue.empty():
          res = queue.get()
          if res is not None:
            break
        tries += 1
      expressions.append((exp, res))
    return expressions
      
  
def load(p):
  name = "expressions_100_para.txt" if p else "expressions_100K_no_para.txt"
  f = open(name, 'r')
  expressions = []
  for pair in f.readlines():
    s = pair.split(' ')
    expressions.append((s[0], float(s[1])))
  f.close()
  return expressions


if __name__ == '__main__':
  print(ExpGen(max_terms=20, parenthesis_prob=0, seed=420).generate(1000))