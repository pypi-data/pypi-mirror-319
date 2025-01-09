from abc import ABC, abstractmethod

from pydantic import BaseModel

from qx_game_bot.core.domain.value_objects.img import Img


class TemplateMatcher(BaseModel, ABC):
    @abstractmethod
    def match(
        self,
        img: str | Img,
        template: str | Img,
        minConfidence: float = None,
        retryCount: int | None = None,
        retryIntervalMS: float = 200,
    ) -> tuple[float, float] | None:
        pass
