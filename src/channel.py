from googleapiclient.discovery import build

class Channel:
    """Класс для ютуб-канала"""

    def __init__(self, channel_id: str, api_key: str) -> None:
        """Экземпляр инициализируется id канала и ключом API."""
        self.youtube = build('youtube', 'v3', developerKey=api_key)
        self.channel_id = channel_id

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
        channel_info = self.get_channel_info()

        if channel_info:
            snippet = channel_info['snippet']
            statistics = channel_info['statistics']

            print(f"Title: {snippet['title']}")
            print(f"Description: {snippet['description']}")
            print(f"View Count: {statistics['viewCount']}")
            print(f"Subscriber Count: {statistics['subscriberCount']}")
            print(f"Video Count: {statistics['videoCount']}")
        else:
            print("Channel not found or API key is invalid.")
