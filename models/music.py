from dataclasses import dataclass
from queue import Queue
from typing import Literal, TypedDict


@dataclass
class MusicEvent:
    source: str
    title: str
    type_url: Literal["audio", "video", "spotify"]


class InstanceParams(TypedDict):
    event_queue: Queue
    music_queue: Queue
    mode: Literal["discord", "spotify"]
