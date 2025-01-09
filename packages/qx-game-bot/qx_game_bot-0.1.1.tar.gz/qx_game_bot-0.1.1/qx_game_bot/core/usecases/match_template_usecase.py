from pydantic import BaseModel

from qx_game_bot.core.domain.value_objects.img import Img
from qx_game_bot.core.ports.screenshot import Screenshot
from qx_game_bot.core.ports.template_matcher import TemplateMatcher


class MatchTemplateUsecase(BaseModel):
    templateMatcher: TemplateMatcher

    def execute(
        self,
        img: str | Img,
        template: str | Img,
        minConfidence=0.9,
        retryCount=None,
        retryIntervalMS=200,
    ):
        res = self.templateMatcher.match(
            img, template, minConfidence, retryCount, retryIntervalMS
        )
        if res is None:
            return None
        confidence, loc = res
        return confidence, loc
