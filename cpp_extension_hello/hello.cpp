#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <iostream>
using std::cout;
using std::endl;

static PyObject* cpp_extension_hello(PyObject* self, PyObject* args) {
  const char* name = nullptr;
  if (!PyArg_ParseTuple(args, "s", &name)) {
    return nullptr;
  }

  cout << "[cpp_extension_hello] hello, " << name << endl;

  PyObject* res_dict = PyDict_New();
  PyObject* name_py = Py_BuildValue("s", name);
  PyObject* age_py = Py_BuildValue("i", 18);
  PyDict_SetItemString(res_dict, "name", name_py);
  PyDict_SetItemString(res_dict, "age", age_py);

  return res_dict;
}

static PyMethodDef cpp_extension_methods[] = {
    {"hello_from_cpp_extension", cpp_extension_hello, METH_VARARGS,
     "Print a hello message"},
    {NULL, NULL, 0, NULL}  // Sentinel is required
};

static struct PyModuleDef cpp_extension_module = {
    PyModuleDef_HEAD_INIT, "hello_cpp_extension", NULL, -1,
    cpp_extension_methods  // comment to regulate the behavior of clang-format
};

PyMODINIT_FUNC PyInit_hello_cpp_extension() {
  return PyModule_Create(&cpp_extension_module);
}
