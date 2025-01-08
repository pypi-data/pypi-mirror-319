from dataclasses import dataclass


@dataclass
class RuTrackerTorrentFile:
	name: str
	is_folder: bool
	files: list
	size: int
