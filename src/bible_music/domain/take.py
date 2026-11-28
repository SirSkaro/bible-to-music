from dataclasses import dataclass

from .arrangement import ArrangementRevision


@dataclass(frozen=True)
class AudioRevisionRef:
    """The take identity and key of one exact audio revision."""

    take_id: str
    revision: str


@dataclass(frozen=True)
class Take:
    arrangement_revision: ArrangementRevision
    original_audio: AudioRevisionRef
