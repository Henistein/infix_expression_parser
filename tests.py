import unittest
import time
from exp_gen import ExpGen, load
from exp_eval import ExpEval
from not_mine2 import Solution

import sys
sys.setrecursionlimit(1000000)


class TestEvaluation(unittest.TestCase):
  EXPRESSION_NUMBER = 100
  """
  def test_evaluation(self):
    exp_gen = ExpGen()
    exp_eval = ExpEval()

    print('Generating 100 expressions...')
    expressions = exp_gen.generate(TestEvaluation.EXPRESSION_NUMBER)
    assert len(expressions) == TestEvaluation.EXPRESSION_NUMBER, 'Not enough expressions generated'

    print('Evaluating %d expressions...' % TestEvaluation.EXPRESSION_NUMBER)

    xp = "(90-((((74)))))"
    xp = "80-93-(98+57*29)+62"
    #xp = "80-93-1751.0+62"
    #xp = "80+(-93)+(-1751.0)+62"
    expressions = [[xp, eval(xp)]]

    for pair in expressions:
      exp = pair[0]
      gt = pair[1]
      res = exp_eval.evaluate(exp)
      self.assertEqual(gt, res, 'Evaluation failed for expression: %s' % exp)
  """
  
  def test_par(self):
    print('Parenthesis:')
    expressions = load(True)
    #expressions = ExpGen(max_terms=100, parenthesis_prob=0.5, max_number=1000).generate(100)

    myeval = ExpEval()
    print('New Mine:')
    start = time.time()
    for pair in expressions:
      #print(pair)
      solved = float(myeval.new_evaluate(pair[0]))
      if round(solved, 3) != round(pair[1], 3):
        print("Expression: %s\nOutput: %s\nExpected: %s" % (pair[0], solved, pair[1]))
    print("Time: %s" % (time.time() - start))

    print('Eval:')
    start = time.time()
    for pair in expressions:
      solved = eval(pair[0])
      if round(solved, 3) != round(pair[1], 3):
        print("Expression: %s\nOutput: %s\nExpected: %s" % (pair[0], solved, pair[1]))
    print("Time: %s" % (time.time() - start))

  def test_no_par(self):
    print('No Parenthesis:')
    expressions = load(False)

    myeval = ExpEval()
    print('New Mine:')
    start = time.time()
    for pair in expressions:
      solved = myeval.new_solve(pair[0])
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


if __name__ == "__main__":
  unittest.main()