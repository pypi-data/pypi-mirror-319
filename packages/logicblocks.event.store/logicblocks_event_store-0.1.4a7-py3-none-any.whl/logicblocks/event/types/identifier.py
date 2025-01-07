import json
from abc import ABC, abstractmethod
from dataclasses import dataclass


class Identifier(ABC):
    @abstractmethod
    def json(self) -> str:
        raise NotImplementedError()


@dataclass(frozen=True)
class Log(Identifier):
    def json(self) -> str:
        return json.dumps({"type": "log"})

    def __repr__(self) -> str:
        return "identifier.Log()"

    def __hash__(self):
        return hash(self.json())


@dataclass(frozen=True)
class Category(Identifier):
    category: str

    def json(self) -> str:
        return json.dumps(
            {
                "type": "category",
                "category": self.category,
            }
        )

    def __repr__(self) -> str:
        return f"identifier.Category(category={self.category})"

    def __hash__(self):
        return hash(self.json())


@dataclass(frozen=True)
class Stream(Identifier):
    category: str
    stream: str

    def json(self) -> str:
        return json.dumps(
            {
                "type": "stream",
                "category": self.category,
                "stream": self.stream,
            }
        )

    def __repr__(self) -> str:
        return (
            f"identifier.Stream(category={self.category},stream={self.stream})"
        )

    def __hash__(self):
        return hash(self.json())


def target(
    *, category: str | None = None, stream: str | None = None
) -> Log | Category | Stream:
    if category is not None and stream is not None:
        return Stream(category=category, stream=stream)
    elif category is not None:
        return Category(category=category)
    elif stream is not None:
        raise ValueError(
            "Invalid target, if stream provided, category must also be provided"
        )
    else:
        return Log()
