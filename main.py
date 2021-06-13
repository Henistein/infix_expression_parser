from string import ascii_lowercase
from itertools import product

#E = '((9 + 9) * (8 - 7)) / (8 - 9)'
#E = '2 * 5 + 3 - 2 * (8 / (4 / 2)) + (3 * 3)'
E = '(() * (8 - 7)) / (8 - 9)'
#---------------Validation-and-Auxiliar-Functions---------------#
# generate vars
def generate_vars():
  for length in range(1, 3):
    for combo in product(ascii_lowercase, repeat=length):
      yield ''.join(combo)
var = generate_vars()

# Parentheses Validation
def pv(E):
  count = 0
  for i in E:
    if i == '(':
      count += 1 
    if i == ')':
      count -= 1
    if count < 0:
      return count
  return count

# operation-number validation
def on_validation(E):
  # remove all the parentheses
  E = E.replace('(', "").replace(')', "")
  # convert all the operations into 'o'
  s = list(E)
  for i in range(len(E)):
    if s[i] in ['+', '-', '/', '*', '^']:
      s[i] = 'o' 

  i = s.count('o') + 1
  while i:
    print(s, i)
    if ''.join([str(elem) for elem in s]).isdigit():
      return 1

    if not ''.join([str(elem) for elem in s[:s.index('o')]]).isdigit():
      return 0 
    s = s[s.index('o')+1:]
    i -= 1
  return 0

# check validation
def check_validation(E):
  if pv(E) == 1:
    return on_validation(E)
  return 0

# auxiliar function that replace character at index
def replace_index(string, position, new_character):
  return string[:position] + new_character + string[position+1:]

# auxiliar function that gives the index of the final '('
# assuming that Expression is valid
def p_final_index(E):
  if '(' in E:
    count = 1
    for i in range(E.index('(')+1, len(E)):
      if E[i] == '(':
        count += 1
      if E[i] == ')':
        count -= 1
      if count == 0:
        return i
  return -1

#---------------Parser---------------#

# replace content inside ()
# assuming that Expression is valid
V = {} # dictionary to store variables
def rcip(E):
  if '(' in E: # since it has a '(' and it is valid we assume that is has a ')'
    # index of ')' match 
    pf = p_final_index(E)
    # inside ( 'content' )
    content = E[E.index('(')+1:pf]
    # remove '(' and ')'
    E = replace_index(E, pf, "")
    E = replace_index(E, E.index('('), "")
    # replace the content in E 
    E = E.replace(content, rcip(content))
    return rcip(E)
  else:
    # generate the new var
    gv = var.__next__()
    V[gv] = E
    return gv

# Infix tree
# assuming that the expresssion is valid
def infix(E):

  # Check if E is a number or a variable  
  if E.isdigit():
    return float(E)
  elif len(E) == 1:
    return infix(V[E])
  else:

    if '+' in E:
      i = E.index('+')
      return infix(E[:i]) + infix(E[i+1:])
    elif '-' in E:
      i = E.index('-')
      return infix(E[:i]) - infix(E[i+1:])
    elif '*' in E:
      i = E.index('*')
      return infix(E[:i]) * infix(E[i+1:])
    elif '/' in E:
      i = E.index('/')
      return infix(E[:i]) / infix(E[i+1:])
    elif '^' in E:
      i = E.index('^')
      return infix(E[:i]) ** infix(E[i+1:])
    else:
      return 0


E = E.replace(' ', '')
#print("Expr: ", E)
#print("Equation: ", V[rcip(E)])
#print("Res: ", infix(V[rcip(E)]))

print(check_validation(E))

