test1 = "80-93-1751.0+62", -1720
test2 = "-80-93-1751.0+62", -1862
test3 = "-80-93-1751.0*62/2", eval("-80-93-1751.0*62/2")
test4 = "-80-93-1751.0/62*2", eval("-80-93-1751.0/62*2")


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

def _solve(exp):
  if '+' not in exp and '*' not in exp and '/' not in exp:
    assert len(exp) == 1, 'Invalid expression:  %s' % exp
    return exp

  if '*' in exp or '/' in exp:
    op_idx_times = ret_index(exp, '*')
    op_idx_div = ret_index(exp, '/')
    if op_idx_div == -1 or (op_idx_times < op_idx_div and op_idx_times != -1):
      exp = perform_op(exp, op_idx_times-1, op_idx_times+1, exp[op_idx_times])
    else:
      exp = perform_op(exp, op_idx_div-1, op_idx_div+1, exp[op_idx_div])
  else:
    exp = perform_op(exp, ret_index(exp, '+')-1, ret_index(exp, '+')+1, '+')

  return _solve(exp)

      
  
print(solve(test1[0]), test1[1])
print(solve(test2[0]), test2[1])
print(solve(test3[0]), test3[1])
print(solve(test4[0]), test4[1])