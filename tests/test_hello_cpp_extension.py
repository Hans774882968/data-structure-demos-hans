from cpp_extension_hello.hello_cpp_extension import hello_from_cpp_extension


def test_hello_from_cpp_extension():
    name = 'hans7'
    res = hello_from_cpp_extension(name)
    assert res['name'] == 'hans7'
    assert res['age'] == 18
