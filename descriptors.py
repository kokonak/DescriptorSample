import inspect
import uuid


class BaseField:
    _default = None

    def __init__(self, default=None, nullable=False):
        """ set default attribute value if default value is None

        :param default: default value of field

        """

        self.nullable = nullable

        if default is not None:
            self._default = default

    def __get__(self, instance, owner):
        if instance is None:
            return self

        if self.name not in instance.__dict__:
            instance.__dict__[self.name] = self._check_nullable(self._get_default())

        return instance.__dict__[self.name]

    def __set__(self, instance, value):
        if self.nullable and value is None and self._default is None:
            return

        instance.__dict__[self.name] = self._value_check(self._check_nullable(value))

    def __set_name__(self, owner, name):
        self.name = name

    def _check_nullable(self, value):
        if not self.nullable and value is None:
            raise Exception(f'`{self.name}` field does not allow None:')

        return value

    def _get_default(self):
        """ return default value of descriptor.
        if default value is callable object, return result of execution the callable object

        :return: default value of descriptor
        """

        if callable(self._default):
            return self._default()
        else:
            return self._default

    def _value_check(self, value):
        """ implement validation logic in here

        :param value:
        :return:
        """
        raise NotImplementedError


class DeviceField(BaseField):
    def _value_check(self, value):
        try:
            if value.lower() not in ['ios', 'android']:
                raise BaseException(f'`{value}` is an invalid device')
        except:
            raise BaseException(f'`{value}` is an invalid parameter')

        return value


class IntegerField(BaseField):
    def _value_check(self, value):
        if type(value) == str and not value.isnumeric():
            raise BaseException(f'`{value}` is not an integer')

        if value:
            try:
                value = int(value)
            except (ValueError, TypeError):
                raise BaseException(f'`{value}` is an invalid parameter')

        return value


class PositiveIntegerField(IntegerField):
    def _value_check(self, value):
        value = super(PositiveIntegerField, self)._value_check(value)
        if value and value < 0:
            raise BaseException(f'`{value}` is not a positive integer')

        return value


class StringField(BaseField):
    length = PositiveIntegerField(nullable=True)

    def __init__(self, default=None, nullable=False, length=None):
        self.length = length
        super().__init__(default=default, nullable=nullable)

    def _value_check(self, value):
        if type(value) != str:
            raise BaseException(f'`{value}` is not a str')

        if self.length and len(value) > self.length:
            raise BaseException(f'value must be less than {self.length}. but value length is {len(value)}')

        return value
