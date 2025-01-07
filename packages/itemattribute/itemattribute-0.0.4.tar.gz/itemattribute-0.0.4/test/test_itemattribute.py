import pytest
from itemattribute import ItemAttribute


def test_set_item():
    ia = ItemAttribute()
    ia['a'] = 1
    assert ia.a == 1, 'Set item failed to assign to attribute'


def test_set_int_error():
    with pytest.raises(TypeError):
        ia = ItemAttribute()
        ia[1] = 1


def test_set_attribute():
    ia = ItemAttribute()
    ia.a = 1
    assert ia['a'] == 1, 'Set attribute failed to assign to attribute'


def test_del_item():
    ia = ItemAttribute()
    ia['a'] = 1
    del ia['a']
    with pytest.raises(AttributeError):
        assert ia.a, 'Del item failed to remove attribute'


def test_del_attribute():
    ia = ItemAttribute()
    ia.a = 1
    del ia.a
    with pytest.raises(AttributeError):
        assert ia['a'], 'Del attribute failed to remove item'


def test_keys():
    ia = ItemAttribute()
    ia.a = 1
    ia.b = 2
    assert set(ia.keys()) == {'a', 'b'}, 'Keys failed to return keys'

    ia = ItemAttribute()
    ia['a'] = 1
    ia['b'] = 2
    assert set(ia.keys()) == {'a', 'b'}, 'Keys failed to return keys'


def test_values():
    ia = ItemAttribute()
    ia.a = 1
    ia.b = 2
    assert set(ia.values()) == {1, 2}, 'Values failed to return values'

    ia = ItemAttribute()
    ia['a'] = 1
    ia['b'] = 2
    assert set(ia.values()) == {1, 2}, 'Values failed to return values'


def test_items():
    ia = ItemAttribute()
    ia.a = 1
    ia.b = 2
    assert set(ia.items()) == {('a', 1), ('b', 2)}, 'Items failed to return items'

    ia = ItemAttribute()
    ia['a'] = 1
    ia['b'] = 2
    assert set(ia.items()) == {('a', 1), ('b', 2)}, 'Items failed to return items'


def test_contains():
    ia = ItemAttribute()
    ia.a = 1
    assert 'a' in ia, 'Contains failed to return True'

    ia = ItemAttribute()
    ia['a'] = 1
    assert 'a' in ia, 'Contains failed to return True'


def test_setattr_overload():

    class NewItemAttribute():
        def __setattr__(self, key, value):
            if isinstance(value, (int, float)):
                self.__dict__[key + 'p1'] = value + 1
            self.__dict__[key] = value

    newia = NewItemAttribute()
    newia.a = 1
    assert newia.a == 1, 'Set attribute failed to assign to attribute'
    assert newia.ap1 == 2, 'Set attribute failed to assign extra attribute'