from dataclasses import dataclass


@dataclass
class NNMClubTorrentFile:
	name: str
	is_folder: bool
	files: list
	size: int
	