from dataclasses import dataclass
from datetime import datetime
from typing import List

from torrent_tracker_search.source.rutracker.model.RuTrackerAuthorLink import RuTrackerAuthorLink
from torrent_tracker_search.source.rutracker.model.RuTrackerForumLink import RuTrackerForumLink


@dataclass
class RuTrackerSearchItem:
	id: int  # id for download torrent file
	is_verified: bool
	name: str
	author: RuTrackerAuthorLink
	forum: RuTrackerForumLink
	tags: List[str]
	size: int
	seed_count: int
	leech_count: int
	download_count: int
	added_at: datetime
