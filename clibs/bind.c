#include "expressions.h"

char get_parenthesis_index_docs[] = "Get indexes of the next parenthesis in expression";

PyMethodDef expressions_funcs[] = {
  {
    "get_parenthesis_index",
    (PyCFunction)get_parenthesis_index,
    METH_VARARGS,
    get_parenthesis_index_docs
  }
};

char expressions_mod_docs[] = "Expressions module";

PyModuleDef expressions_mod = {
  PyModuleDef_HEAD_INIT,
  "expressions",
  expressions_mod_docs,
  -1,
  expressions_funcs,
  NULL,
  NULL,
  NULL,
  NULL

};

PyMODINIT_FUNC PyInit_expressions(void){
  return PyModule_Create(&expressions_mod);
}