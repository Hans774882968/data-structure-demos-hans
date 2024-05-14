from setuptools import setup, find_packages, Extension


def get_long_description():
    with open('README.md', 'r', encoding='utf-8') as f:
        content = f.read()
        return content


long_description = get_long_description()

extensions = [
    Extension(
        'binary_indexed_tree.bit_cpp_extension',
        [
            'binary_indexed_tree/bit.cpp',
        ],
        language='c++'
    ),
    Extension(
        'cpp_extension_hello.hello_cpp_extension',
        [
            'cpp_extension_hello/hello.cpp',
        ],
        language='c++'
    ),
    Extension(
        'bisect_decr.bisect_decr_cpp',
        [
            'bisect_decr/bisect_decr.cpp'
        ],
        language='c++'
    )
]

setup(
    name='data-structure-demos-hans',
    version='0.2.0',
    description='provide some data structures for competitive programming',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='hans',
    author_email='774882968@qq.com',
    url='https://github.com/Hans774882968/data-structure-demos-hans',
    packages=find_packages('.'),
    include_package_data=True,
    license='MIT',
    ext_modules=extensions,
)
