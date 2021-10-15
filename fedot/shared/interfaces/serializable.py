from abc import ABC, abstractmethod
from dataclasses import is_dataclass
from importlib import import_module
from inspect import signature
from typing import Any, Dict

DELIMITER = '/'
CLASS_PATH_KEY = '_class_path'


class Serializable(ABC):

    @abstractmethod
    def to_json(self) -> Dict[str, Any]:
        return {
            **vars(self),
            CLASS_PATH_KEY: f'{self.__module__}{DELIMITER}{self.__class__.__qualname__}'
        }

    @classmethod
    @abstractmethod
    def from_json(cls, json_obj: Dict[str, Any]) -> Any:
        init_data = {
            k: v
            for k, v in json_obj.items()
            if k in signature(cls.__init__).parameters
        }
        obj = cls(**init_data)
        vars(obj).update(json_obj)
        return obj
