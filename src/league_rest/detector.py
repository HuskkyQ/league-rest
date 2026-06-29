from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
import math
from typing import Optional, Sequence


class ChampionState(str, Enum):
    ALIVE = "alive"
    DEAD = "dead"
    UNKNOWN = "unknown"


@dataclass(frozen=True)
class DetectorSample:
    values: Sequence[float]


@dataclass(frozen=True)
class DetectorConfig:
    alive_reference: DetectorSample
    dead_reference: DetectorSample
    max_distance: float
    min_margin: float


class DeathRespawnDetector:
    def __init__(self, config: DetectorConfig) -> None:
        self._config = config

    def detect(self, sample: Optional[DetectorSample]) -> ChampionState:
        if sample is None:
            return ChampionState.UNKNOWN

        alive_distance = _distance(sample, self._config.alive_reference)
        dead_distance = _distance(sample, self._config.dead_reference)
        nearest_distance = min(alive_distance, dead_distance)

        if nearest_distance > self._config.max_distance:
            return ChampionState.UNKNOWN

        if alive_distance == dead_distance:
            return ChampionState.UNKNOWN

        if abs(alive_distance - dead_distance) < self._config.min_margin:
            return ChampionState.UNKNOWN

        if alive_distance < dead_distance:
            return ChampionState.ALIVE

        return ChampionState.DEAD


def _distance(left: DetectorSample, right: DetectorSample) -> float:
    if len(left.values) != len(right.values):
        raise ValueError("Detector samples must have the same length")

    return math.sqrt(sum((a - b) ** 2 for a, b in zip(left.values, right.values)))
