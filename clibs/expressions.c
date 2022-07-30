#include <stdio.h>
#include <Python.h>
#include "expressions.h"

PyObject *get_parenthesis_index(PyObject *self, PyObject *args) {
  PyObject *str;
  if (!PyArg_ParseTuple(args, "O", &str)) {
    return NULL;
  }

  const char *cstr = PyUnicode_AsUTF8(str);
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

PyObject *ultra_split(PyObject *self, PyObject *args) {
  PyObject *str;
  if (!PyArg_ParseTuple(args, "O", &str)) {
    return NULL;
  }

  const char *cstr = PyUnicode_AsUTF8(str);
  if (cstr == NULL) {
    return NULL;
  }

  // create a list to store the split strings
  PyObject *list = PyList_New(0);

  int aux = 0;
  int last_i = 0;
  for(int i=0; cstr[i]; i++){
    switch (cstr[i]){
    case '-': 
      if(i == 0 || cstr[i-1] == '*' || cstr[i-1] == '/' || cstr[i-1] == 'e'){
        continue;
      }
      else if(cstr[i+1] == '-'){
        // copy from aux to i-1
        PyList_Append(list, PyUnicode_FromStringAndSize(cstr+aux, i-aux));
        i += 2;
        aux = i;
      }
      else{
        PyList_Append(list, PyUnicode_FromStringAndSize(cstr+aux, i-aux));
        aux = i;
      }
      break;
    
    case '+':
      if(i == 0 || cstr[i-1] == '*' || cstr[i-1] == '/' || cstr[i-1] == 'e'){
        continue;
      }
      else{
        PyList_Append(list, PyUnicode_FromStringAndSize(cstr+aux, i-aux));
        i++;
        aux = i;
      }
      break;
    
    default:
      break;
    }
    last_i = i;
  }
  // split last expression
  PyList_Append(list, PyUnicode_FromStringAndSize(cstr+aux, last_i-aux+1));


  return list;

}


PyObject *is_number(PyObject *self, PyObject *args){
  PyObject *str;
  if (!PyArg_ParseTuple(args, "O", &str)) {
    return NULL;
  }

  const char *cstr = PyUnicode_AsUTF8(str);
  if (cstr == NULL) {
    return NULL;
  }

  for(int i=0; cstr[i]; i++){
    if(cstr[i] == '*' || cstr[i] == '/'){
      //return Py_BuildValue("i", 0);
      Py_RETURN_FALSE;
    }
  }
  Py_RETURN_TRUE;
}

PyObject *operate_times_div(PyObject *self, PyObject *args){
  PyObject *str;
  if (!PyArg_ParseTuple(args, "O", &str)) {
    return NULL;
  }

  const char *cstr = PyUnicode_AsUTF8(str);
  if (cstr == NULL) {
    return NULL;
  }

  int aux = 0;
  int last_op = -1; // -1 for None, 0 for *, 1 for /
  double last_number = .0;
  int last_i = 0;

  for(int i=0; i<cstr[i]; i++){
    //printf("%f\n", last_number);
    if(cstr[i] == '*' || cstr[i] == '/'){
      if(last_op == 0){
        last_number *= atof(memcpy(malloc(i-aux+1), cstr+aux, i-aux));
        aux = i+1;
      }
      else if(last_op == 1){
        last_number /= atof(memcpy(malloc(i-aux+1), cstr+aux, i-aux));
        aux = i+1;
      }
      else{
        last_number = atof(memcpy(malloc(i-aux+1), cstr+aux, i-aux+1));
        aux = i+1;
      }
      if(cstr[i] == '*'){
        last_op = 0;
      }
      else{
        last_op = 1;
      }
    }
    last_i = i;
  }
  int i = last_i;
  if(last_op == 0){
    last_number *= atof(cstr+aux);
  }
  else if(last_op == 1){
    last_number /= atof(cstr+aux);
  }
  else{
    last_number = atof(cstr+aux);
  }

  // return last number double
  return PyFloat_FromDouble(last_number);
}