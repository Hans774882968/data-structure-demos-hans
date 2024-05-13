#define PY_SSIZE_T_CLEAN
#include <Python.h>

static PyMethodDef cppExtensionMethods[] = {
    {nullptr, nullptr, 0, nullptr}  // Sentinel is required
};

struct BITObject {
  PyObject_HEAD int n;
  int* a;
};

static void bit_dealloc(BITObject* self) {
  delete[] self->a;
  Py_TYPE(self)->tp_free(self);
}

static PyObject* bit_new(PyTypeObject* type, PyObject* args, PyObject* kwds) {
  BITObject* self = (BITObject*)type->tp_alloc(type, 0);
  int n = 0;
  if (!PyArg_ParseTuple(args, "i", &n)) {
    Py_DECREF(self);
    return nullptr;
  }
  self->n = n;
  self->a = new int[n + 1]();
  return (PyObject*)self;
}

static bool jdg_idx(BITObject* self, int idx) {
  if (idx < 0) {
    PyErr_SetString(PyExc_ValueError,
                    "idx should be greater than or equal to 0");
    return false;
  }
  if (idx > self->n) {
    PyErr_SetString(PyExc_ValueError,
                    "idx should be less than or equal to array size");
    return false;
  }
  return true;
}

static PyObject* bit_add(BITObject* self, PyObject* args, PyObject* kwds) {
  int idx = 0, v = 0;
  if (!PyArg_ParseTuple(args, "ii", &idx, &v)) {
    return nullptr;
  }

  if (!jdg_idx(self, idx)) {
    return nullptr;
  }

  for (; idx <= self->n; idx += idx & -idx) self->a[idx] += v;

  Py_RETURN_NONE;
}

static PyObject* bit_sum(BITObject* self, PyObject* args, PyObject* kwds) {
  int idx = 0;
  if (!PyArg_ParseTuple(args, "i", &idx)) {
    return nullptr;
  }

  if (!jdg_idx(self, idx)) {
    return nullptr;
  }

  int res = 0;
  for (; idx; idx -= idx & -idx) res += self->a[idx];
  PyObject* res_py = PyLong_FromLong(res);
  return res_py;
}

static PyMethodDef bit_methods[] = {
    {"sum", (PyCFunction)bit_sum, METH_VARARGS | METH_KEYWORDS,
     "Queries prefix sum"},
    {"add", (PyCFunction)bit_add, METH_VARARGS | METH_KEYWORDS,
     "Performs the add operation"},
    {nullptr},  // Sentinel is required
};

static PyTypeObject BitType = {
    PyVarObject_HEAD_INIT(NULL, 0) "binary_indexed_tree.bit_cpp_extension.BIT",
    sizeof(BITObject),
    .tp_dealloc = (destructor)bit_dealloc,
    .tp_flags = Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE,
    .tp_doc = "Binary Indexed Tree",
    .tp_methods = bit_methods,
    .tp_new = bit_new,
};

static struct PyModuleDef cpp_extension_module = {
    PyModuleDef_HEAD_INIT, "bit_cpp_extension", NULL, -1, cppExtensionMethods};

PyMODINIT_FUNC PyInit_bit_cpp_extension() {
  PyObject* m = nullptr;
  if (PyType_Ready(&BitType) < 0) {
    return nullptr;
  }
  m = PyModule_Create(&cpp_extension_module);
  if (m == nullptr) {
    return nullptr;
  }
  Py_INCREF(&BitType);
  if (PyModule_AddObject(m, "BIT", (PyObject*)&BitType) < 0) {
    Py_DECREF(&BitType);
    Py_DECREF(m);
    return nullptr;
  }
  return m;
}
