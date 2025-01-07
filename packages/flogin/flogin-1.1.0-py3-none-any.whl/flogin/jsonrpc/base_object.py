import json
from typing import Any, Self

__all__ = ("Base",)


class Base:
    __slots__ = ()
    __jsonrpc_option_names__: dict[str, str] = {}

    def to_dict(self) -> dict:
        foo = {}
        for name in self.__slots__:
            item = getattr(self, name)
            if isinstance(item, Base):
                item = item.to_dict()
            elif item and isinstance(item, list) and isinstance(item[0], Base):
                item = [item.to_dict() for item in item]
            foo[self.__jsonrpc_option_names__.get(name, name)] = item
        return foo

    @classmethod
    def from_dict(cls: type[Self], data: dict[str, Any]) -> Self:
        raise RuntimeError("This should be overriden")

    def __repr__(self) -> str:
        args = []
        for item in self.__slots__:
            args.append(f"{item}={getattr(self, item)!r}")
        return f"<{self.__class__.__name__} {' '.join(args)}>"


class ToMessageBase(Base):
    def to_message(self, id: int) -> bytes:
        return (json.dumps(self.to_dict()) + "\r\n").encode()
