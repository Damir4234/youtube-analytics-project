import json
from googleapiclient.discovery import build

class Channel:
    """Класс для ютуб-канала"""

    def __init__(self, channel_id: str, api_key: str) -> None:
        """Экземпляр инициализируется id канала и ключом API."""
        self.youtube = build('youtube', 'v3', developerKey=api_key)
        self.channel_id = channel_id
        self.channel_info = self.get_channel_info()

        if self.channel_info:
            snippet = self.channel_info['snippet']
            statistics = self.channel_info['statistics']
            self.title = snippet['title']
            self.description = snippet['description']
            self.view_count = statistics['viewCount']
            self.subscriber_count = statistics['subscriberCount']
            self.video_count = statistics['videoCount']
            self.url = f"https://www.youtube.com/channel/{self.channel_id}"

    def get_channel_info(self) -> dict:
        """Получает информацию о канале с использованием API YouTube."""
        request = self.youtube.channels().list(
            part='snippet,statistics',
            id=self.channel_id
        )
        response = request.execute()
        return response.get('items')[0] if response.get('items') else None

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        if self.channel_info:
            print(f"Title: {self.title}")
            print(f"Description: {self.description}")
            print(f"View Count: {self.view_count}")
            print(f"Subscriber Count: {self.subscriber_count}")
            print(f"Video Count: {self.video_count}")
            print(f"URL: {self.url}")
        else:
            print("Channel not found or API key is invalid.")

    @classmethod
    def get_service(cls, api_key: str):
        """Возвращает объект для работы с YouTube API."""
        return build('youtube', 'v3', developerKey=api_key)

    def to_json(self, filename: str) -> None:
        """Сохраняет значения атрибутов экземпляра в файл JSON."""
        data = {
            "channel_id": self.channel_id,
            "title": self.title,
            "description": self.description,
            "view_count": self.view_count,
            "subscriber_count": self.subscriber_count,
            "video_count": self.video_count,
            "url": self.url
        }

        with open(filename, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)