from dataclasses import dataclass
from datetime import datetime

from torrent_tracker_search.source.nnmclub.model.NNMClubAuthorLink import NNMClubAuthorLink
from torrent_tracker_search.source.nnmclub.model.NNMClubForumLink import NNMClubForumLink
from torrent_tracker_search.source.nnmclub.model.NNMClubTopicLink import NNMClubTopicLink


@dataclass
class NNMClubSearchItem:
	id: int  # id for download torrent file
	author: NNMClubAuthorLink
	forum: NNMClubForumLink
	topic: NNMClubTopicLink
	size: int
	seed_count: int
	leech_count: int
	added_at: datetime
