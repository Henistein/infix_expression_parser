#include <stdio.h>
#include <Python.h>
#include "expressions.h"

PyObject *get_parenthesis_index(PyObject *self, PyObject *args) {
  PyObject *str;
  if (!PyArg_ParseTuple(args, "O", &str)) {
    return NULL;
  }

  char *cstr = PyUnicode_AsUTF8(str);
  if (cstr == NULL) {
    return NULL;
  }

  int i1 = -1, i2 = -1;
  int count = 0;

  for(int i=0; cstr[i]; i++){
    if(cstr[i] == '('){
      count++;
      if(i1 == -1){
        i1 = i;
      }
    }
    else if(cstr[i] == ')'){
      count--;
    }
    if(count == 0 && i1 != -1){
      i2 = i;
      break;
    }
  }

  // return a tuple with the indexes of the parenthesis
  PyObject *tuple = PyTuple_New(2);
  PyTuple_SetItem(tuple, 0, PyLong_FromLong(i1));
  PyTuple_SetItem(tuple, 1, PyLong_FromLong(i2));
  return tuple;
}
