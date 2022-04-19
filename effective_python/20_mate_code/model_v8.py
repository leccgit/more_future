from collections import OrderedDict


class Validated:
    pass


class EntityMeta(type):
    @classmethod
    def __prepare__(metacls, name, bases):
        return OrderedDict()

    def __init__(cls, name, bases, attr_dict):
        super(EntityMeta, cls).__init__(name, bases, attr_dict)
        cls._field_names = []
        for key, attr in attr_dict.items():
            if isinstance(attr, Validated):
                type_name = type(attr).__name__
                attr.storage_name = '_{}#{}'.format(type_name, key)
                cls._field_names.append(key)

        print("hello world")


class Entity(metaclass=EntityMeta):
    """带有验证字段的业务实体"""

    @classmethod
    def field_names(cls):
        for name in cls._field_names:
            yield name
