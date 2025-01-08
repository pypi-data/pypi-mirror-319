from urllib.parse import urlparse

from bs4 import Tag


def get_forum_id(forum_td: Tag) -> int:
	forum_href = forum_td.div.a["href"]
	query = urlparse(forum_href).query.split("&")
	for item in query:
		if item.startswith("f="):
			query_name, query_value = item.split("=")
			return int(query_value)
	raise Exception(f"Error on get forum id from {forum_href}")

def get_user_id(author_td: Tag) -> int:
	author_href = author_td.div.a["href"]
	query = urlparse(author_href).query.split("&")
	for item in query:
		if item.startswith("pid="):
			query_name, query_value = item.split("=")
			return int(query_value)
	raise Exception(f"Error on get author id from {author_td}")

