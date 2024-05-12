#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <iostream>
#include <vector>

const char* lower_bound_intro =
    "The return value i is such that all e in a[:i] have e > x, and all e in "
    "a[i:] have e <= x";
const char* upper_bound_intro =
    "The return value i is such that all e in a[:i] have e >= x, and all e in "
    "a[i:] have e < x";

static bool jdg_arr(PyObject* a_py) {
  if (!PyList_Check(a_py)) {
    PyErr_SetString(PyExc_ValueError,
                    "Plz pass an integer array and an integer");
    return false;
  }
  int n = PyList_GET_SIZE(a_py);
  for (size_t i = 0; i < n; i++) {
    PyObject* num_py = PyList_GET_ITEM(a_py, i);
    if (!PyLong_Check(num_py)) {
      PyErr_SetString(PyExc_ValueError,
                      "Every elements of the array should be integer");
      return false;
    }
  }
  return true;
}

static PyObject* dec_lower_bound(PyObject* self, PyObject* args) {
  PyObject* a_py = nullptr;
  int x = 0;
  if (!PyArg_ParseTuple(args, "Oi", &a_py, &x)) {
    PyErr_SetString(PyExc_ValueError,
                    "Plz pass an integer array and an integer");
    return nullptr;
  }
  if (!jdg_arr(a_py)) {
    return nullptr;
  }

  int n = PyList_GET_SIZE(a_py);
  std::vector<int> a;
  for (size_t i = 0; i < n; i++) {
    PyObject* num_py = PyList_GET_ITEM(a_py, i);
    int num = PyLong_AS_LONG(num_py);
    a.push_back(num);
  }

  int l = 0, r = n;
  while (l < r) {
    int mid = (l + r) >> 1;
    if (a[mid] > x) {
      l = mid + 1;
    } else {
      r = mid;
    }
  }

  PyObject* res_py = PyLong_FromLong(l);
  return res_py;
}

static PyObject* dec_upper_bound(PyObject* self, PyObject* args) {
  PyObject* a_py = nullptr;
  int x = 0;
  if (!PyArg_ParseTuple(args, "Oi", &a_py, &x)) {
    PyErr_SetString(PyExc_ValueError,
                    "Plz pass an integer array and an integer");
    return nullptr;
  }
  if (!jdg_arr(a_py)) {
    return nullptr;
  }

  int n = PyList_GET_SIZE(a_py);
  std::vector<int> a;
  for (size_t i = 0; i < n; i++) {
    PyObject* num_py = PyList_GET_ITEM(a_py, i);
    int num = PyLong_AS_LONG(num_py);
    a.push_back(num);
  }

  int l = 0, r = n;
  while (l < r) {
    int mid = (l + r) >> 1;
    if (a[mid] >= x) {
      l = mid + 1;
    } else {
      r = mid;
    }
  }

  PyObject* res_py = PyLong_FromLong(l);
  return res_py;
}

static PyMethodDef cppExtensionMethods[] = {
    {"dec_lower_bound", dec_lower_bound, METH_VARARGS, lower_bound_intro},
    {"dec_upper_bound", dec_upper_bound, METH_VARARGS, upper_bound_intro},
    {NULL, NULL, 0, NULL}  // Sentinel is required
};

static struct PyModuleDef cpp_extension_module = {
    PyModuleDef_HEAD_INIT, "bisect_decr_cpp", NULL, -1, cppExtensionMethods};

PyMODINIT_FUNC PyInit_bisect_decr_cpp() {
  return PyModule_Create(&cpp_extension_module);
}
