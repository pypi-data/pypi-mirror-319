

class ItemAttribute(object):
    '''
    Class that has properties which can be called like dictionary
    items

    Parameters
    ----------
    dictionary : dict
        Dictionary object, defaults to None, contains initial
        attributes for ItemAttribute instance.

    '''

    def __init__(self, dictionary=None):
        if dictionary is not None:
            for k in dictionary.keys():
                self[k] = dictionary[k]

    def __getitem__(self, key):
        '''
        Maps self[key] to the self.__getattribute__ method.
        '''
        return self.__getattribute__(key)

    def __setitem__(self, key, value):
        '''
        Maps self[key] = value to the self.__setattr__ method.
        '''
        self.__setattr__(key, value)

    def __delitem__(self, key):
        '''
        Maps del self[key] to the self.__delattr__ method.
        '''
        self.__delattr__(key)

    def keys(self):
        '''
        Returns a list of keys.
        '''
        return self.__dict__.keys()

    def values(self):
        '''
        Returns a list of values.
        '''
        return self.__dict__.values()

    def items(self):
        '''
        Returns a list of key:value pairs.
        '''
        return self.__dict__.items()

    def __contains__(self, item):
        '''
        Overloads the `key in object` syntax to check if
        `key in obj.__dict__`
        '''

        return item in self.__dict__
