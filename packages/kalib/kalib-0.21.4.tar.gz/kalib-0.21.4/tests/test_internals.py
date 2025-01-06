import syspath  # noqa: F401

from kalib.internals import Is, Who


class DummyClass:
    def __init__(self, value):
        self.value = value

def test_is_with_address():
    obj = DummyClass(10)
    result = Is(obj, addr=True)
    assert result.startswith(f'({Who(obj)}#')

def test_is_without_address():
    obj = DummyClass(10)
    result = Is(obj, addr=False)
    assert result == f'({Who.Is(obj, addr=False)})'

def test_is_with_json():
    obj = DummyClass(10)
    result = Is(obj, addr=True)
    assert result.startswith(f'{Who(obj)}#')
    assert 'value' in result

def test_is_with_class():
    obj = DummyClass
    result = Is(obj, addr=True)
    assert result.startswith(f'{Who(obj)}#')

def test_is_with_none():
    obj = None
    result = Is(obj, addr=True)
    assert result.startswith(f'{Who(obj)}#')
