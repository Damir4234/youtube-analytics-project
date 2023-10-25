import os
from googleapiclient.discovery import build


class Video:
    """Класс для работы с видео из YouTube."""
    __YT_API_KEY = os.getenv('api_you')

    def __init__(self, video_id: str) -> None:
        """Видео инициализируется ID и далее через API."""
        self.__video_id = video_id
        self._init_from_api()

    def _init_from_api(self):
        """Получаем данные по API и инициализируем экземпляр класса ими."""
        service = self.get_service()
        try:
            video_response = service.videos().list(
                part='snippet,statistics',
                id=self.__video_id
            ).execute()

            video_data = video_response['items'][0]
            snippet = video_data['snippet']
            statistics = video_data['statistics']

            self.title = snippet['title']
            self.url = f'https://youtu.be/{self.__video_id}'
            self.view_count = statistics['viewCount']
            self.like_count = statistics['likeCount']
        except Exception as e:
            self.title = None
            self.url = None
            self.view_count = None
            self.like_count = None

    @classmethod
    def get_service(cls) -> build:
        """Возвращает объект для работы с YouTube API."""
        service = build('youtube', 'v3', developerKey=cls.__YT_API_KEY)
        return service

    def __str__(self) -> str:
        return self.title
