from typing import Literal
import numpy as np
from pydantic import BaseModel

from qx_game_bot.adapters.cv.cv_template_matcher import CvTemplateMatcher
from qx_game_bot.adapters.mss.mss_screenshot import MssScreenshot
from qx_game_bot.adapters.persistence.sqlite import db
from qx_game_bot.adapters.persistence.sqlite.sqlite_task_repository import (
    SqliteTaskRepository,
)
from qx_game_bot.adapters.pynput.pynput_action_player import PynputActionPlayer
from qx_game_bot.adapters.pynput.pynput_keyboard_mouse_listener import (
    PynputKeyboardMouseListener,
)
from qx_game_bot.core.domain.value_objects.delay_action import DelayAction
from qx_game_bot.core.domain.value_objects.key_press_action import KeyPressAction
from qx_game_bot.core.domain.value_objects.key_release_action import KeyReleaseAction
from qx_game_bot.core.domain.value_objects.key_tap_action import KeyTapAction
from qx_game_bot.core.domain.value_objects.key_type_action import KeyTypeAction
from qx_game_bot.core.domain.value_objects.mouse_move_action import MouseMoveAction
from qx_game_bot.core.domain.value_objects.mouse_press_action import MousePressAction
from qx_game_bot.core.domain.value_objects.mouse_release_action import (
    MouseReleaseAction,
)
from qx_game_bot.core.domain.value_objects.mouse_scroll_action import MouseScrollAction
from qx_game_bot.core.domain.value_objects.mouse_tap_action import MouseTapAction
from qx_game_bot.core.ports.screenshot import MonitorRegion
from qx_game_bot.core.usecases.match_screen_usecase import MatchScreenUsecase
from qx_game_bot.core.usecases.match_template_usecase import MatchTemplateUsecase
from qx_game_bot.core.usecases.play_action_usecase import PlayActionUsecase
from qx_game_bot.core.usecases.play_task_usecase import PlayTaskUsecase
from qx_game_bot.core.usecases.record_task_usecase import RecordTaskUsecase


class QxGameBotFramework:
    def __init__(self, dbFilePath: str = ":memory:"):
        db.database.init(dbFilePath)
        sqliteTaskRepository = SqliteTaskRepository()
        pynputKeyboardMouseListener = PynputKeyboardMouseListener()
        pynputActionPlayer = PynputActionPlayer()
        cvTemplateMatcher = CvTemplateMatcher()
        mssScreenshot = MssScreenshot()
        self._recordTaskUsecase = RecordTaskUsecase(
            taskRepository=sqliteTaskRepository,
            keyboardMouseActionListener=pynputKeyboardMouseListener,
        )
        self._playTaskUsecase = PlayTaskUsecase(actionPlayer=pynputActionPlayer)
        self._playActionUsecase = PlayActionUsecase(actionPlayer=pynputActionPlayer)
        self._matchTemplateUsecase = MatchTemplateUsecase(
            templateMatcher=cvTemplateMatcher
        )
        self._matchScreenUsecase = MatchScreenUsecase(
            templateMatcher=cvTemplateMatcher, screenshot=mssScreenshot
        )

    def delay(self, timeoutMS: float):
        self._playActionUsecase.execute(DelayAction(timeoutMS=timeoutMS))
        return self

    def keyPress(self, key: str):
        self._playActionUsecase.execute(KeyPressAction(key=key))
        return self

    def keyRelease(self, key: str):
        self._playActionUsecase.execute(KeyReleaseAction(key=key))
        return self

    def keyReleaseAll(self):
        unReleasedActinons = []
        for action in self._playActionUsecase.playedActions:
            if isinstance(action, KeyPressAction):
                unReleasedActinons.append(action)
            if (
                isinstance(action, KeyReleaseAction)
                and KeyPressAction(**action.model_dump()) in unReleasedActinons
            ):
                unReleasedActinons.remove(KeyPressAction(**action.model_dump()))
        for action in unReleasedActinons:
            self._playActionUsecase.execute(KeyReleaseAction(**action.model_dump()))
        return self

    def keyTap(self, key: str, count: int = 1, intervalMS=None):
        for i in range(count):
            self._playActionUsecase.execute(KeyTapAction(key=key))
            if intervalMS:
                self._playActionUsecase.execute(DelayAction(timeoutMS=intervalMS))
        return self

    def keyTapAll(self, *keys: str, count: int = 1, intervalMS=None):
        for i in range(count):
            for key in keys:
                self._playActionUsecase.execute(KeyPressAction(key=key))
            for key in keys:
                self._playActionUsecase.execute(KeyReleaseAction(key=key))
            if intervalMS:
                self._playActionUsecase.execute(DelayAction(timeoutMS=intervalMS))
        return self

    def keyType(self, string: str, count: int = 1, intervalMS=None):
        for i in range(count):
            self._playActionUsecase.execute(KeyTypeAction(string=string))
            if intervalMS:
                self._playActionUsecase.execute(DelayAction(timeoutMS=intervalMS))
        return self

    def mousePress(
        self,
        button: Literal["left", "right", "middle"],
        x: int = None,
        y: int = None,
    ):
        self._playActionUsecase.execute(MousePressAction(button=button, x=x, y=y))
        return self

    def mouseRelease(
        self,
        button: Literal["left", "right", "middle"],
        x: int = None,
        y: int = None,
    ):
        self._playActionUsecase.execute(MouseReleaseAction(button=button, x=x, y=y))
        return self

    def mouseClick(
        self,
        button: Literal["left", "right", "middle"] = "left",
        x: int = None,
        y: int = None,
        count: int = 1,
        intervalMS=None,
    ):
        for i in range(count):
            self._playActionUsecase.execute(MouseTapAction(button=button, x=x, y=y))
            if intervalMS:
                self._playActionUsecase.execute(DelayAction(timeoutMS=intervalMS))
        return self

    def mouseMoveTo(
        self,
        x: int = None,
        y: int = None,
    ):
        self._playActionUsecase.execute(MouseMoveAction(x=x, y=y))
        return self

    def mouseScrollBy(
        self,
        dx: int = None,
        dy: int = None,
        x: int = None,
        y: int = None,
    ):
        self._playActionUsecase.execute(MouseScrollAction(dx=dx, dy=dy, x=x, y=y))
        return self

    def matchScreen(
        self,
        templateImg: str | np.ndarray,
        minConfidence: float | None = 0.9,
        retryCount: int | None = None,
        retryIntervalMS: int | None = 200,
        monitorRegion: MonitorRegion | None = None,
    ):
        if monitorRegion:
            return self._matchScreenUsecase.execute(
                templateImg,
                minConfidence=minConfidence,
                retryCount=retryCount,
                retryIntervalMS=retryIntervalMS,
                monitorRegion=monitorRegion,
            )
        return self._matchScreenUsecase.execute(
            templateImg,
            minConfidence=minConfidence,
            retryCount=retryCount,
            retryIntervalMS=retryIntervalMS,
        )

    def matchTemplate(
        self,
        img: str | np.ndarray,
        templateImg: str | np.ndarray,
        minConfidence: float | None = 0.9,
        retryCount: int | None = None,
        retryIntervalMS: int | None = 200,
    ):
        return self._matchTemplateUsecase.execute(
            img,
            templateImg,
            minConfidence=minConfidence,
            retryCount=retryCount,
            retryIntervalMS=retryIntervalMS,
        )
