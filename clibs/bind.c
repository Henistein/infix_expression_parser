#include "expressions.h"

char get_parenthesis_index_docs[] = "Get indexes of the next parenthesis in expression";
char ultra_split_docs[] = "Ultra Split";
char is_number_docs[] = "Is number";
char operate_times_div_docs[] = "Operate times/div";

PyMethodDef expressions_funcs[] = {
  { "get_parenthesis_index",
    (PyCFunction)get_parenthesis_index,
    METH_VARARGS,
    get_parenthesis_index_docs},
  { "ultra_split",
    (PyCFunction)ultra_split,
    METH_VARARGS,
    ultra_split_docs},
  { "is_number",
    (PyCFunction)is_number,
    METH_VARARGS,
    is_number_docs},
  { "operate_times_div",
    (PyCFunction)operate_times_div,
    METH_VARARGS,
    operate_times_div_docs},
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