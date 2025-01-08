# Torrent Tracker Search Lib

## Integrations

- rutracker.org
- nnmclub.to

## Example

```python
from torrent_tracker_search.ClientBuilder import ClientBuilder
from torrent_tracker_search.source.rutracker.RuTrackerService import RuTrackerService
from torrent_tracker_search.source.rutracker.RuTrackerClient import RuTrackerClient
from torrent_tracker_search.source.nnmclub.NNMClubService import NNMClubService
from torrent_tracker_search.source.nnmclub.NNMClubClient import NNMClubClient

builder = ClientBuilder()
rutracker_client, nnmclub_client = builder.build(clients=[RuTrackerClient(), NNMClubClient()])
rutracker_service = RuTrackerService(rutracker_client)
nnmclub_service = NNMClubService(rutracker_client)


async def main(query: str):
    await rutracker_service.login(login="", password="")
    nnmclub_service.login(session_id="")
    result_from_rutracker = await rutracker_service.search(query)
    result_from_nnmclub = await nnmclub_service.search(query)
    print(f"{result_from_rutracker=}")
    print(f"{result_from_nnmclub=}")
    await builder.session.close()


```