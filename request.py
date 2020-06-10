from descriptors import BaseField


class BaseRequest:
    _desc_attributes = None

    def __init__(self, data: dict):
        # set data to attributes

        self._desc_attributes = []
        for attr_name in self.__dir__():
            attr_value = getattr(type(self), attr_name)

            if isinstance(attr_value, BaseField) or isinstance(attr_value, BaseRequest):
                self._desc_attributes.append(attr_name)

        # set attribute data
        [self.__setattr__(key, data.get(key)) for key in data.keys() if key in self._desc_attributes]

        # set default data and check nullable
        [self.__getattribute__(attr_name) for attr_name in self._desc_attributes]

    def data(self):
        return {attr_name: self.__getattribute__(attr_name) for attr_name in self._desc_attributes}

    def __eq__(self, other):
        try:
            if self.__class__ != other.__class__:
                return False
        except:
            return False

        for attr_name in self._desc_attributes:
            if self.__getattribute__(attr_name) != other.__getattribute__(attr_name):
                return False

        return True
