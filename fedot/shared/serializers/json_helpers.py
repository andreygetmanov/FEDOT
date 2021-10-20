from importlib import import_module
from inspect import isclass, isfunction, ismethod
from typing import Any, Dict
from uuid import UUID

from ..interfaces.serializable import (CLASS_PATH_KEY, DELIMITER, Serializable,
                                       dump_path_to_obj)


def encoder(obj: Any) -> Dict[str, Any]:  # serves as 'default' encoder in json.dumps(...)
    if isinstance(obj, Serializable):
        return obj.to_json()
    elif isinstance(obj, UUID):
        return obj.hex
    elif isfunction(obj) or ismethod(obj):
        return dump_path_to_obj(obj)
    raise TypeError(f'{obj=} can\'t be serialized!')


def _get_class(class_path: str) -> Any:
    module_name, class_name = class_path.split(DELIMITER)
    obj_cls = import_module(module_name)
    for sub in class_name.split('.'):
        obj_cls = getattr(obj_cls, sub)
    return obj_cls


def decoder(json_obj: Dict[str, Any]) -> Any:  # serves as 'object_hook' decoder in json.loads(...)
    if CLASS_PATH_KEY in json_obj:
        obj_cls = _get_class(json_obj[CLASS_PATH_KEY])
        del json_obj[CLASS_PATH_KEY]
        if isclass(obj_cls) and issubclass(obj_cls, Serializable):
                return obj_cls.from_json(json_obj)
        elif isfunction(obj_cls) or ismethod(obj_cls):
            return obj_cls
        raise TypeError(f'Parsed {obj_cls=} is not serializable, but should be')
    return json_obj
