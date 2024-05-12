[TOC]

# 用C++编写Python扩展，并用setuptools打包自己的分发包

## 引言

最近手痒想写Python和C++代码，于是有了这篇~~精华~~水blog。这次打算用C++写些数据结构，打包后给Python调用。

[项目GitHub传送门](https://github.com/Hans774882968/data-structure-demos-hans)

## 环境

- Windows10 VSCode
- Python 3.7.6 pytest 7.4.4 setuptools 68.0.0
- `g++.exe (x86_64-win32-seh-rev1, Built by MinGW-Builds project) 13.1.0` from [here](https://whitgit.whitworth.edu/tutorials/installing_mingw_64)

## 制作源码包

我们可以用`setuptools`制作源码包。项目目录：

```
.
│  setup.py 调用 setuptools.setup
├─binary_indexed_tree
      bit.py 最简单的命令行程序
      __init__.py 留空就行。为了让 setuptools 扫描到这个包，必须要有
```

`setup.py`：

```python
from setuptools import setup, find_packages, Extension

setup(
    name='data-structure-demos-hans',
    version='0.1',
    description='provide some data structures for competitive programming',
    author='hans',
    author_email='774882968@qq.com',
    url='https://github.com/Hans774882968/data-structure-demos-hans',
    packages=find_packages('.'),
    license='MIT',
)
```

制作源码包命令：`python setup.py sdist`。

```
running sdist
running egg_info
creating data_structure_demos_hans.egg-info
writing data_structure_demos_hans.egg-info\PKG-INFO
writing dependency_links to data_structure_demos_hans.egg-info\dependency_links.txt
writing top-level names to data_structure_demos_hans.egg-info\top_level.txt
writing manifest file 'data_structure_demos_hans.egg-info\SOURCES.txt'
reading manifest file 'data_structure_demos_hans.egg-info\SOURCES.txt'
writing manifest file 'data_structure_demos_hans.egg-info\SOURCES.txt'
running check
creating data-structure-demos-hans-0.1
creating data-structure-demos-hans-0.1\binary_indexed_tree
creating data-structure-demos-hans-0.1\data_structure_demos_hans.egg-info
copying files to data-structure-demos-hans-0.1...
copying README.md -> data-structure-demos-hans-0.1
copying setup.py -> data-structure-demos-hans-0.1
copying binary_indexed_tree\__init__.py -> data-structure-demos-hans-0.1\binary_indexed_tree
copying binary_indexed_tree\bit.py -> data-structure-demos-hans-0.1\binary_indexed_tree 
copying data_structure_demos_hans.egg-info\PKG-INFO -> data-structure-demos-hans-0.1\data_structure_demos_hans.egg-info
copying data_structure_demos_hans.egg-info\SOURCES.txt -> data-structure-demos-hans-0.1\data_structure_demos_hans.egg-info
copying data_structure_demos_hans.egg-info\dependency_links.txt -> data-structure-demos-hans-0.1\data_structure_demos_hans.egg-info
copying data_structure_demos_hans.egg-info\top_level.txt -> data-structure-demos-hans-0.1\data_structure_demos_hans.egg-info
Writing data-structure-demos-hans-0.1\setup.cfg
creating dist
Creating tar archive
removing 'data-structure-demos-hans-0.1' (and everything under it)
```

运行完毕后生成dist目录和data_structure_demos_hans.egg-info目录。`dist`目录下有`data-structure-demos-hans-0.1.tar.gz`，这就是我们的源码包。

接下来运行`pip install data-structure-demos-hans-0.1.tar.gz`安装刚刚打好的包：

```
Looking in indexes: https://mirrors.aliyun.com/pypi/simple
Processing <project dir>\dist\data-structure-demos-hans-0.1.tar.gz
  Preparing metadata (setup.py) ... done
Building wheels for collected packages: data-structure-demos-hans
  Building wheel for data-structure-demos-hans (setup.py) ... done
  Created wheel for data-structure-demos-hans: filename=data_structure_demos_hans-0.1-py3-none-any.whl size=1943 sha256=14aa4f5dff5de02c7d2e6125ef3c0127ec6466a97929573b355545fea9800b3f
  Stored in directory: <%homepath%>\appdata\local\pip\cache\wheels\47\64\58\02429501ec651b154a43b87f2630ad2d34b69df5fb31ee1d49
Successfully built data-structure-demos-hans
Installing collected packages: data-structure-demos-hans
Successfully installed data-structure-demos-hans-0.1
```

运行`pip list`可看到这一行`data-structure-demos-hans 0.1`已经出现。此时进入`<python install dir>\Lib\site-packages`可以看到`binary_indexed_tree`文件夹和`data_structure_demos_hans-0.1.dist-info`文件夹。因此，调用树状数组的代码可以这么写：

```python
from binary_indexed_tree.bit import BIT


def main():
    a1 = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
    b1 = BIT(len(a1))
    for i, v in enumerate(a1):
        b1.add(i + 1, v)
    for i in range(1, len(a1) + 1):
        print(b1.sum(i))


if __name__ == '__main__':
    main()
```

## C/C++扩展 Hello World

新增文件夹`cpp_extension_hello`：

```
cpp_extension_hello
    hello.cpp
    __init__.py 空文件
```

和上一章类似，我们只需要修改`setup.py`和`hello.cpp`。先看`setup.py`的改动：

```python
from setuptools import setup, find_packages, Extension

extensions = [
    Extension(
        'cpp_extension_hello.hello_cpp_extension',
        [
            'cpp_extension_hello/hello.cpp',
        ],
        language='c++'
    ),
]

setup(
    # omit other params
    ext_modules=extensions,
)
```

`Extension`类代表一个C/C++模块。这里指定了模块名`hello_cpp_extension`，那么链接时就会去找`PyInit_hello_cpp_extension`这个函数，这个函数用于模块初始化。如果打算写C模块，可以省略`language='c++'`。

在写C++代码前，最好先让VSCode能够找到`Python.h`。这次我们先不用cmake，而是选择一个更轻量的方案：配置`.vscode\c_cpp_properties.json`。`Ctrl+Shift+P`选择`C/C++ Edit Configurations`，会自动生成上述文件。

```json
{
    "configurations": [
        {
            // ...
            "includePath": [
                "${workspaceFolder}/**",
                "<python install path>\\include" // Python.h 所在的目录
            ],
            "intelliSenseMode": "windows-gcc-x64",
            "compilerPath": "<your mingw64 path>\\bin\\g++"
        }
    ],
    // ...
}
```

接下来看`hello.cpp`：

```cpp
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
```

注意点：

1. 这个文件格式有一些要求，我模仿着[参考链接3](https://codedamn.com/news/python/implementing-custom-python-c-extensions-step-by-step-guide)写的。
2. `static struct PyModuleDef cpp_extension_module`的`m_name`应该要和`setup.py`指定的一致？TODO
3. `cppExtensionMethods`的哨兵是必要的，否则运行时会报错`module functions cannot set METH_CLASS or METH_STATIC`。
4. `PyMethodDef.ml_name`指定了模块调用者使用的方法名为`hello_from_cpp_extension`。

在此我希望用我本地的g++来编译cpp，所以需要建一个`setup.cfg`：

```properties
[build]
compiler=mingw32
```

之后，我们执行`python setup.py sdist`并不会编译cpp，因为这个编译过程发生在`pip install data-structure-demos-hans-0.1.tar.gz`阶段。接下来如果不出意外的话，就要出意外了TAT。`pip install`报错：

```
        File "<python install dir>\lib\distutils\cygwinccompiler.py", line 86, in get_msvcr
          raise ValueError("Unknown MS Compiler version %s " % msc_ver)
      ValueError: Unknown MS Compiler version 1916
```

幸好，经过一番搜索，找到了[参考链接2](https://blog.51cto.com/lang13002/6723721)。按其指示，我们新增一小段代码就OK：

```python
        elif msc_ver == '1916':
            # manually add because "Unknown MS Compiler version 1916". VS2015
            return ['msvcr120']
```

`pip install`成功情况下的输出如下：

```
Looking in indexes: https://mirrors.aliyun.com/pypi/simple
Processing <project dir>\dist\data-structure-demos-hans-0.1.tar.gz
  Preparing metadata (setup.py) ... done
Building wheels for collected packages: data-structure-demos-hans
  Building wheel for data-structure-demos-hans (setup.py) ... done
  Created wheel for data-structure-demos-hans: filename=data_structure_demos_hans-0.1-cp37-cp37m-win_amd64.whl size=23786 sha256=96cfef2a169f3edda75a86d8303fee8724b7b32bcb496328d7161404807cce85
  Stored in directory: <%homepath%>\appdata\local\pip\cache\wheels\47\64\58\02429501ec651b154a43b87f2630ad2d34b69df5fb31ee1d49
Successfully built data-structure-demos-hans
Installing collected packages: data-structure-demos-hans
  Attempting uninstall: data-structure-demos-hans
    Found existing installation: data-structure-demos-hans 0.1
    Uninstalling data-structure-demos-hans-0.1:
      Successfully uninstalled data-structure-demos-hans-0.1
Successfully installed data-structure-demos-hans-0.1
```

安装成功后，可以找到一个pyd文件`<python install path>\Lib\site-packages\cpp_extension_hello\hello_cpp_extension.cp37-win_amd64.pyd`。最后写段代码调用一下：

```python
from cpp_extension_hello.hello_cpp_extension import hello_from_cpp_extension


def main():
    hello_from_cpp_extension('hans')


if __name__ == '__main__':
    main()
```

### Optional：类型提示支持

虽然调用成功了，但是没有类型提示，不太友好。首先我们需要加一个`.pyi`文件。`.pyi`文件的名字要和import的文件名一致，所以文件名是`hello_cpp_extension`。`hello_cpp_extension.pyi`：

```python
def hello_from_cpp_extension(name: str) -> None:
    pass
```

接下来我们要把`.pyi`文件打包进去，但默认情况下它不会被打包进去。根据[参考链接4](https://github.com/pypa/setuptools/issues/3136)，如果你的`setuptools`版本大于等于`69.0.0`，那么可以比较容易地做到这件事。但我的是`68.0.0`，因此需要：

1. 传递选项`include_package_data=True`。
2. 新增`MANIFEST.in`：

```properties
recursive-include * *.pyi
```

之后再打包，就能看到`.pyi`文件被打包进去了。

Q：不需要加一个空的`py.typed`文件？A：是的。本项目场景比较简单，暂时不需要理会PEP-561规范。

## 用C++扩展实现树状数组

`binary_indexed_tree`目录新增两个文件`bit.cpp`和`bit_cpp_extension.pyi`：

```
binary_indexed_tree
    bit.cpp
    bit.py
    bit_cpp_extension.pyi
    __init__.py
```

`setup.py`例行更改`extensions`数组：

```python
extensions = [
    Extension(
        'binary_indexed_tree.bit_cpp_extension',
        [
            'binary_indexed_tree/bit.cpp',
        ],
        language='c++'
    ),
    # ...
]
```

在C++扩展中定义一个Python数据结构至少需要定义两个数据结构，类类型数据结构和对象类型数据结构。

对象类型数据结构用来装你需要的数据，但是必须包含一个`PyObject_HEAD`头部。本章新增的对象类型数据结构如下：

```cpp
struct BITObject {
  PyObject_HEAD int n;
  int* a;
};
```

类类型数据结构是一个`PyTypeObject`类型的实例。这家伙有相当多的字段，但在本例中我们需要提供的很少。结合一个叫`pysegmenttree`的项目（[具体参考的代码传送门](https://github.com/greshilov/pysegmenttree/blob/master/pysegmenttree/_extensions/intsegmenttree.h)）和[参考链接5](https://zhuanlan.zhihu.com/p/106773873)，和上面定义的对象类型数据结构，本章新增的类类型数据结构**主要**需要提供的字段只有`tp_dealloc`、`tp_flags`、`tp_doc`、`tp_methods`、`tp_new = bit_new`。其他字段都保持为nullptr即可。

```cpp
static PyTypeObject BitType = {
    PyVarObject_HEAD_INIT(NULL, 0) "binary_indexed_tree.bit_cpp_extension.BIT",
    sizeof(BITObject),
    .tp_dealloc = (destructor)bit_dealloc,
    .tp_flags = Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE,
    .tp_doc = "Binary Indexed Tree",
    .tp_methods = bit_methods,
    .tp_new = bit_new,
};
```



1. `PyVarObject_HEAD_INIT(NULL, 0)`是固定写法。
2. 根据参考链接5，`tp_name = binary_indexed_tree.bit_cpp_extension.BIT`不是随意定义的字符串。它应对应Python调用者的import方式`from binary_indexed_tree.bit_cpp_extension import BIT`。
3. `tp_basicsize`指定为`sizeof(对象类型数据结构)`。
4. `tp_doc`随意写即可。

接下来咱把目光放到模块初始化函数。相比于上一章的一句话`return PyModule_Create(&cpp_extension_module);`，这次的代码量要大得多了，但也是看着参考链接5和`pysegmenttree`项目，按格式来即可。

```cpp
PyMODINIT_FUNC PyInit_bit_cpp_extension() {
  PyObject* m;
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
```

我们接着看类类型数据结构涉及的几个对象和方法。

`bit_methods`：我们希望提供的类的成员方法。

```cpp
static PyMethodDef bit_methods[] = {
    {"sum", (PyCFunction)bit_sum, METH_VARARGS | METH_KEYWORDS,
     "Queries prefix sum"},
    {"add", (PyCFunction)bit_add, METH_VARARGS | METH_KEYWORDS,
     "Performs the add operation"},
    {nullptr},  // Sentinel is required
};
```

`bit_sum`、`bit_add`的函数签名模仿着参考链接5写就行。`bit_sum`、`bit_add`和它们共用的入参校验逻辑`jdg_idx`如下：

```cpp
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
```

这里用到了几个API：

1. `PyArg_ParseTuple`用来拿入参。`ii`表示取两个int。
2. `PyErr_SetString`用来抛异常。这里我抛出了`ValueError`。
3. 因为几个方法返回值都得是`PyObject*`，所以需要用`PyLong_FromLong`把C++的int转为`PyObject*`。

抽象出`jdg_idx`的过程：原本的写法是：

```cpp
  if (idx < 0) {
    PyErr_SetString(PyExc_ValueError,
                    "idx should be greater than or equal to 0");
    return nullptr;
  }
```

那么我们可以将其变为`PyErr_SetString; return false/true; return nullptr;`，于是可以抽象出一个返回`bool`的函数，然后这么调用：

```cpp
  if (!jdg_idx(self, idx)) {
    return nullptr;
  }
```

`bit_new`：进行对象的初始化工作。除了`type->tp_alloc(type, 0)`是没见过的固定写法外，其他内容我们都比较熟悉了。`tp_alloc`顾名思义就是给对象类型数据结构分配内存。

```cpp
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
```

`bit_dealloc`：进行堆内存释放工作，依据参考链接5，不写也能跑，但会造成内存泄露。

```cpp
static void bit_dealloc(BITObject* self) {
  delete[] self->a;
  Py_TYPE(self)->tp_free(self);
}
```

即使我们不提供该函数，Python解释器也会调用`Py_TYPE(self)->tp_free(self)`。但我们提供该函数后，就不得不手动加上这句话了。

最后按惯例，展示一下我们刚刚实现的树状数组的用法：

```python
from binary_indexed_tree.bit_cpp_extension import BIT


def bit_cpp(a: List[int]):
    b1 = BIT(len(a))
    for i, v in enumerate(a):
        b1.add(i + 1, v)
    for i in range(1, len(a) + 1):
        print(b1.sum(i))
    b1.add(9, 113964)
    print(b1.sum(len(a)))
    b2 = BIT(20)
    try:
        b2.add(-2, 10)
    except ValueError as e:
        print(e)
    try:
        b2.sum(-1)
    except ValueError as e:
        print(e)
    try:
        b2.sum(22)
    except ValueError as e:
        print(e)
    try:
        b2.add(21, 10)
    except ValueError as e:
        print(e)
    b2.add(2, 20)
    b2.add(4, 30)
    print(b2.sum(5))  # 50
```

## 餐后甜点：用C++扩展实现单调递减数组的二分查找函数

本节我们模仿`bisect`包的API，用C++扩展实现单调递减数组的二分查找函数。

### 支持int数组的二分查找

新增模块`bisect_decr_cpp`，提供的方法如下：

```cpp
const char* lower_bound_intro =
    "The return value i is such that all e in a[:i] have e > x, and all e in "
    "a[i:] have e <= x";
const char* upper_bound_intro =
    "The return value i is such that all e in a[:i] have e >= x, and all e in "
    "a[i:] have e < x";

static PyMethodDef cppExtensionMethods[] = {
    {"dec_lower_bound", dec_lower_bound, METH_VARARGS, lower_bound_intro},
    {"dec_upper_bound", dec_upper_bound, METH_VARARGS, upper_bound_intro},
    {NULL, NULL, 0, NULL}  // Sentinel is required
};
```

`dec_lower_bound`和`dec_upper_bound`几乎完全一致，我们以`dec_lower_bound`为例。

```cpp
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
```

在此我们看到一个具有普适性的规律：C++代码和Python代码属于两个抽象层，因此我们的工作流程一般如下：先把Python抽象层的语言翻译为C++抽象层的语言，接着判断参数的合法性，然后做些计算，最后再翻译回Python抽象层的语言。

1. 抽象出`jdg_arr`的思路同上一节。
2. `PyList_Check, PyLong_Check`用于校验参数类型，`PyList_GET_SIZE`拿列表长度，`PyList_GET_ITEM`根据下标拿列表元素。

最后按惯例，展示一下其用法：

```python
from bisect_decr.bisect_decr_cpp import dec_lower_bound, dec_upper_bound


def case1():
    a = [100, 90, 80, 70, 60, 50, 40, 30, 20, 10]
    l1 = dec_lower_bound(a, 101)
    l2 = dec_lower_bound(a, 61)
    l3 = dec_lower_bound(a, 9)
    l4 = dec_lower_bound(a, 100)
    l5 = dec_lower_bound(a, 60)
    l6 = dec_lower_bound(a, 10)
    u1 = dec_upper_bound(a, 101)
    u2 = dec_upper_bound(a, 61)
    u3 = dec_upper_bound(a, 9)
    u4 = dec_upper_bound(a, 100)
    u5 = dec_upper_bound(a, 60)
    u6 = dec_upper_bound(a, 10)
    print(l1, l2, l3, l4, l5, l6)  # 0 4 10 0 4 9
    print(u1, u2, u3, u4, u5, u6)  # 0 4 10 1 5 10


def case2():
    a = [90, 90, 90, 80, 80, 70]
    l1 = dec_lower_bound(a, 91)
    l2 = dec_lower_bound(a, 90)
    l3 = dec_lower_bound(a, 85)
    l4 = dec_lower_bound(a, 80)
    l5 = dec_lower_bound(a, 75)
    l6 = dec_lower_bound(a, 70)
    l7 = dec_upper_bound(a, 60)
    u1 = dec_upper_bound(a, 91)
    u2 = dec_upper_bound(a, 90)
    u3 = dec_upper_bound(a, 85)
    u4 = dec_upper_bound(a, 80)
    u5 = dec_upper_bound(a, 75)
    u6 = dec_upper_bound(a, 70)
    u7 = dec_upper_bound(a, 60)
    print(l1, l2, l3, l4, l5, l6, l7)  # 0 0 3 3 5 5 6
    print(u1, u2, u3, u4, u5, u6, u7)  # 0 3 3 5 5 6 6


def main():
    case1()
    case2()


if __name__ == '__main__':
    main()
```

### 支持任意可比较对象的数组的二分查找

TODO

## 单测：pytest

```bash
pip install -U pytest
pip install -U pytest-html
# 测试安装是否成功
pytest --version
```

常规的断言使用`assert`关键字就行。异常断言的写法：`with pytest.raises(ValueError) as e_info: # write code here that might throw an exception`。举例：

```python
    b2 = BIT(20)
    with pytest.raises(ValueError) as e_info:
        b2.add(-2, 10)
    assert 'idx should be greater than or equal to 0' in str(e_info.value)
```

运行单测命令：

```bash
pytest --html=coverage/report.html
```

## 参考资料

1. Python使用setuptools打包自己的分发包并使用举例：https://blog.csdn.net/hxxjxw/article/details/124298543
2. Windows10下用mingw编译python扩展库：https://blog.51cto.com/lang13002/6723721
3. https://codedamn.com/news/python/implementing-custom-python-c-extensions-step-by-step-guide
4. Include type information by default (`*.pyi`, `py.typed`)：https://github.com/pypa/setuptools/issues/3136
5. 使用c/c++编写python扩展（三）：自定义Python内置类型：https://zhuanlan.zhihu.com/p/106773873