from enum import Enum
from typing import Self

from pydantic import BaseModel


class Tag(BaseModel):
    id: int | None
    name: str

    def __eq__(self, other) -> bool:
        if isinstance(other, Tag):
            return self.name == other.name
        raise NotImplementedError

    def __hash__(self):
        return hash(self.name)


class CommandStatus(str, Enum):
    SUCCESS = "SUCCESS"
    NEW = "NEW"
    FAILED = "FAILED"


class TradingAssetCommandLog(BaseModel):
    command_id: str  # unique, uuid compliant
    reason: str | None
    status: CommandStatus

    @classmethod
    def get_new(cls, command_id: str) -> Self:
        return cls(
            command_id=command_id,
            status=CommandStatus.NEW,
        )
