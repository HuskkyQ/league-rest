from league_rest.detector import (
    ChampionState,
    DeathRespawnDetector,
    DetectorConfig,
    DetectorSample,
)


def _detector():
    return DeathRespawnDetector(
        DetectorConfig(
            alive_reference=DetectorSample((0.8, 0.6, 0.2)),
            dead_reference=DetectorSample((0.2, 0.1, 0.8)),
            max_distance=0.25,
            min_margin=0.1,
        )
    )


def test_calibrated_alive_sample_returns_alive():
    assert _detector().detect(DetectorSample((0.78, 0.59, 0.22))) == ChampionState.ALIVE


def test_calibrated_dead_sample_returns_dead():
    assert _detector().detect(DetectorSample((0.22, 0.11, 0.79))) == ChampionState.DEAD


def test_far_sample_returns_unknown():
    assert _detector().detect(DetectorSample((0.5, 0.9, 0.9))) == ChampionState.UNKNOWN


def test_ambiguous_margin_returns_unknown():
    detector = DeathRespawnDetector(
        DetectorConfig(
            alive_reference=DetectorSample((0.0,)),
            dead_reference=DetectorSample((1.0,)),
            max_distance=1.0,
            min_margin=0.2,
        )
    )

    assert detector.detect(DetectorSample((0.45,))) == ChampionState.UNKNOWN


def test_missing_sample_returns_unknown():
    assert _detector().detect(None) == ChampionState.UNKNOWN


def test_state_sequence_from_fixture_values():
    detector = _detector()
    samples = [
        DetectorSample((0.8, 0.6, 0.2)),
        DetectorSample((0.2, 0.1, 0.8)),
        DetectorSample((0.5, 0.9, 0.9)),
        DetectorSample((0.79, 0.61, 0.21)),
    ]

    assert [detector.detect(sample) for sample in samples] == [
        ChampionState.ALIVE,
        ChampionState.DEAD,
        ChampionState.UNKNOWN,
        ChampionState.ALIVE,
    ]


def test_max_distance_boundary_is_exclusive():
    detector = DeathRespawnDetector(
        DetectorConfig(
            alive_reference=DetectorSample((0.0,)),
            dead_reference=DetectorSample((1.0,)),
            max_distance=0.2,
            min_margin=0.01,
        )
    )

    assert detector.detect(DetectorSample((0.21,))) == ChampionState.UNKNOWN


def test_exact_tie_returns_unknown_even_without_margin():
    detector = DeathRespawnDetector(
        DetectorConfig(
            alive_reference=DetectorSample((0.0,)),
            dead_reference=DetectorSample((1.0,)),
            max_distance=1.0,
            min_margin=0.0,
        )
    )

    assert detector.detect(DetectorSample((0.5,))) == ChampionState.UNKNOWN
