from services.queue.music import MusicQueueManager
from services.youtube import Youtube


class SearchController:
    def __init__(self, queue_manager_provider=MusicQueueManager()):
        self.queue_manager = queue_manager_provider

    def search_music(self, search: str):

        songs = (
            Youtube().search_single_song(search)
            if "https://" not in search
            else Youtube().search_by_link(search)
        )
        self.queue_manager.add_many_songs(songs)
