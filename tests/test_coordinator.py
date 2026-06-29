from league_rest.coordinator import CoordinatorAction, FocusCoordinator
from league_rest.detector import ChampionState


class FocusRecorder:
    def __init__(self):
        self.calls = []

    def focus_browser(self):
        self.calls.append("browser")

    def focus_game(self):
        self.calls.append("game")


def test_alive_dead_alive_switches_once_each_way():
    recorder = FocusRecorder()
    coordinator = FocusCoordinator(recorder.focus_browser, recorder.focus_game)

    actions = [
        coordinator.handle_state(ChampionState.ALIVE),
        coordinator.handle_state(ChampionState.DEAD),
        coordinator.handle_state(ChampionState.ALIVE),
    ]

    assert actions == [
        CoordinatorAction.NONE,
        CoordinatorAction.FOCUS_BROWSER,
        CoordinatorAction.FOCUS_GAME,
    ]
    assert recorder.calls == ["browser", "game"]


def test_repeated_dead_does_not_focus_browser_repeatedly():
    recorder = FocusRecorder()
    coordinator = FocusCoordinator(recorder.focus_browser, recorder.focus_game)

    actions = [
        coordinator.handle_state(ChampionState.ALIVE),
        coordinator.handle_state(ChampionState.DEAD),
        coordinator.handle_state(ChampionState.DEAD),
        coordinator.handle_state(ChampionState.DEAD),
    ]

    assert actions == [
        CoordinatorAction.NONE,
        CoordinatorAction.FOCUS_BROWSER,
        CoordinatorAction.NONE,
        CoordinatorAction.NONE,
    ]
    assert recorder.calls == ["browser"]


def test_repeated_alive_does_not_focus_game_repeatedly():
    recorder = FocusRecorder()
    coordinator = FocusCoordinator(recorder.focus_browser, recorder.focus_game)

    actions = [
        coordinator.handle_state(ChampionState.ALIVE),
        coordinator.handle_state(ChampionState.ALIVE),
    ]

    assert actions == [CoordinatorAction.NONE, CoordinatorAction.NONE]
    assert recorder.calls == []


def test_unknown_does_not_replace_last_confirmed_state():
    recorder = FocusRecorder()
    coordinator = FocusCoordinator(recorder.focus_browser, recorder.focus_game)

    actions = [
        coordinator.handle_state(ChampionState.ALIVE),
        coordinator.handle_state(ChampionState.UNKNOWN),
        coordinator.handle_state(ChampionState.DEAD),
        coordinator.handle_state(ChampionState.UNKNOWN),
        coordinator.handle_state(ChampionState.DEAD),
        coordinator.handle_state(ChampionState.ALIVE),
    ]

    assert actions == [
        CoordinatorAction.NONE,
        CoordinatorAction.NONE,
        CoordinatorAction.FOCUS_BROWSER,
        CoordinatorAction.NONE,
        CoordinatorAction.NONE,
        CoordinatorAction.FOCUS_GAME,
    ]
    assert recorder.calls == ["browser", "game"]


def test_dead_first_event_focuses_browser_once():
    recorder = FocusRecorder()
    coordinator = FocusCoordinator(recorder.focus_browser, recorder.focus_game)

    actions = [
        coordinator.handle_state(ChampionState.UNKNOWN),
        coordinator.handle_state(ChampionState.DEAD),
        coordinator.handle_state(ChampionState.DEAD),
    ]

    assert actions == [
        CoordinatorAction.NONE,
        CoordinatorAction.FOCUS_BROWSER,
        CoordinatorAction.NONE,
    ]
    assert recorder.calls == ["browser"]
