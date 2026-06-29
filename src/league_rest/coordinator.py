from __future__ import annotations

from enum import Enum
from typing import Callable, Optional

from .detector import ChampionState


class CoordinatorAction(str, Enum):
    NONE = "none"
    FOCUS_BROWSER = "focus_browser"
    FOCUS_GAME = "focus_game"


class FocusCoordinator:
    def __init__(self, focus_browser: Callable[[], None], focus_game: Callable[[], None]) -> None:
        self._focus_browser = focus_browser
        self._focus_game = focus_game
        self._last_confirmed_state: Optional[ChampionState] = None

    def handle_state(self, state: ChampionState) -> CoordinatorAction:
        if state == ChampionState.UNKNOWN:
            return CoordinatorAction.NONE

        previous = self._last_confirmed_state
        self._last_confirmed_state = state

        if state == previous:
            return CoordinatorAction.NONE

        if state == ChampionState.DEAD:
            self._focus_browser()
            return CoordinatorAction.FOCUS_BROWSER

        if previous == ChampionState.DEAD and state == ChampionState.ALIVE:
            self._focus_game()
            return CoordinatorAction.FOCUS_GAME

        return CoordinatorAction.NONE
