#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <iostream>

static PyObject* cpp_extension_hello(PyObject* self, PyObject* args) {
  const char* name;

  if (!PyArg_ParseTuple(args, "s", &name)) {
    return nullptr;
  }

  std::cout << "[cpp_extension_hello] hello, " << name << std::endl;

  Py_RETURN_NONE;
}

static PyMethodDef cppExtensionMethods[] = {
    {"hello_from_cpp_extension", cpp_extension_hello, METH_VARARGS,
     "Print a hello message"},
    {NULL, NULL, 0, NULL}  // Sentinel is required
};

static struct PyModuleDef cpp_extension_module = {PyModuleDef_HEAD_INIT,
                                                  "hello_cpp_extension", NULL,
                                                  -1, cppExtensionMethods};

PyMODINIT_FUNC PyInit_hello_cpp_extension() {
  return PyModule_Create(&cpp_extension_module);
}
