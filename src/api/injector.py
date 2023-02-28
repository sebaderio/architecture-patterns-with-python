from typing import Any, Type, TypeVar

from fastapi import Depends, Request

TypeToInject = TypeVar("TypeToInject")


def inject(item: Type[TypeToInject]) -> TypeToInject:
    def inject(request: Request) -> Any:
        return request.app.state.injector.get(item)

    return Depends(inject)
