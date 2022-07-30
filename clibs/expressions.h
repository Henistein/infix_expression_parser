#ifndef __EXPRESSIONS_H__
#define __EXPRESSIONS_H__

#include <Python.h>

PyObject *get_parenthesis_index(PyObject *self, PyObject *args);
PyObject *ultra_split(PyObject *self, PyObject *args);
PyObject *is_number(PyObject *self, PyObject *args);
PyObject *operate_times_div(PyObject *self, PyObject *args);

#endif