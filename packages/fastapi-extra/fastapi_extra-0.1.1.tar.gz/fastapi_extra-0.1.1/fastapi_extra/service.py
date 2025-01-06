__author__ = "ziyan.yin"
__date__ = "2025-01-05"


from abc import ABCMeta
from typing import TYPE_CHECKING, Annotated, Any, Self, Type, TypeVar

from fastapi.params import Depends


class ServiceMetaClass(ABCMeta):
    __root__: Any = None
    
    def __new__(
        mcs,
        name: str,
        bases: tuple[type, ...],
        attrs: dict,
        abstract: bool = False
    ):
        new_cls = super().__new__(mcs, name, bases, attrs)
        
        if not abstract:
            if new_cls.__root__ and issubclass(new_cls, new_cls.__root__.__class__):
                base_cls = new_cls.__root__.__class__
                new_cls.__root__ = None
                new_cls.__root__ = new_cls()
                base_cls.__root__ = new_cls.__root__
            else:
                new_cls.__root__ = None
                new_cls.__root__ = new_cls()
        
        return new_cls
    
    def __call__(cls, *args, **kwargs):
        if cls.__root__ is not None:
            return cls.__root__
        return super().__call__(*args, **kwargs)


class IService(metaclass=ServiceMetaClass, abstract=True):
    
    def _load(self, *args, **kwargs) -> Self:
        return self


S = TypeVar("S", bound=IService)


class Service_:
    
    @classmethod
    def __class_getitem__(cls, item: Type[IService]):
        if not item.__root__:
            raise ImportError(cls.__name__)
        return  Annotated[item, Depends(item.__root__._load)]


if TYPE_CHECKING:
    Service = Annotated[S, None]
else:
    Service = Service_
