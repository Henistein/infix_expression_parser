from string import ascii_lowercase
from itertools import product

#E = '((9 + 9) * (8 - 7)) / (8 - 9)'
#E = '(9 + 9) * (8 - 7)'
E = '(9 + 9) * (9 + 9) + (9 + 9) * (9 + 9) + (9 + 9) * (9 + 9) + (9 + 9) * (9 + 9)'

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

# Infix tree
def it(E):
  if len(E) == 1 and E.isdigit():
    return float(E)

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

    E = E.replace(content, rcip(content))
    return rcip(E)
  else:
    #if any(char.isdigit() for char in E):
      # generate the new var
      gv = var.__next__()
      V[gv] = E
      return gv
    #else:
      #return E

E = E.replace(' ', '')
print(E)
print(V[rcip(E)])
print(V)
