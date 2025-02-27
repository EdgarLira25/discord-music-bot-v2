from dataclasses import dataclass
from typing import Literal


@dataclass
class MusicEvent:
    source: str
    title: str
    type_url: Literal["audio", "video"]
