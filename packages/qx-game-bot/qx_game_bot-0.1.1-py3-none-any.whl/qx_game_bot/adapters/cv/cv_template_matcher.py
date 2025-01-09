from time import sleep
import cv2
from qx_game_bot.core.domain.value_objects.img import Img
from qx_game_bot.core.ports.template_matcher import TemplateMatcher


class CvTemplateMatcher(TemplateMatcher):
    debug: bool | None = None

    def match(self, img, template, minConfidence=0.9):
        if isinstance(img, str):
            imgArr = cv2.imread(img)
            width = imgArr.shape[1]
            height = imgArr.shape[0]
            img = Img(img=imgArr, width=width, height=height)
        if isinstance(template, str):
            tempArr = cv2.imread(template)
            width = tempArr.shape[1]
            height = tempArr.shape[0]
            template = Img(img=tempArr, width=width, height=height)

        res = cv2.matchTemplate(img.img, template.img, cv2.TM_CCOEFF_NORMED)
        minVal, maxVal, minLoc, maxLoc = cv2.minMaxLoc(res)

        if maxVal < minConfidence:
            return None

        if self.debug:
            cv2.imshow("Match", template.img)
            cv2.waitKey(1)

        return maxVal, maxLoc
