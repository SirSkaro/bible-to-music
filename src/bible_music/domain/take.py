from dataclasses import dataclass

from .arrangement import ArrangementRevision


@dataclass(frozen=True)
class AudioRevision:
    take_id: str
    revision: str


@dataclass(frozen=True)
class Take:
    arrangement_revision: ArrangementRevision
    original_audio: AudioRevision
