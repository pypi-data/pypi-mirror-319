import types
from dataclasses import dataclass, fields, is_dataclass
from typing import Mapping, Self


@dataclass
class NestedDeserializableDataclass:
    """
    A dataclass that can be generated from a dict. Fields that are dataclasses
    themselves are properly initialized as well.
    """

    @classmethod
    def from_dict(cls, d: Mapping) -> Self:
        def init_value(type_, value):
            if type(type_) == types.GenericAlias:
                if type_.__origin__ == list:
                    l = []
                    for el in value:
                        l.append(init_value(type_.__args__[0], el))
                    return l
                elif type_.__origin__ == dict:
                    d = {}
                    for k, v in value.items():
                        d[k] = init_value(type_.__args__[1], v)
                    return d
                else:
                    raise TypeError(f"Invalid type for NestedDeserializableDataclass: {type_}")
            elif issubclass(type_, NestedDeserializableDataclass):
                return type_.from_dict(value)
            elif is_dataclass(type_):
                return type_(**value)
            else:
                return value

        d = dict(d)
        for field in fields(cls):
            d[field.name] = init_value(field.type, d[field.name])

        return cls(**d)
