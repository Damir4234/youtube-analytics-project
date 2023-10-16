import requests

class Video:
    def __init__(self, video_id):
        self.video_id = video_id
        self.title, self.views, self.likes = self.get_video_info()

    def get_video_info(self):
        api_key = "AIzaSyAuL2OjFeSiPj6_RbqicyelyX0pmeDkboA"
        url = f'https://www.googleapis.com/youtube/v3/videos?key={api_key}&part=snippet,statistics&id={self.video_id}'
        response = requests.get(url)
        data = response.json()

        if 'items' in data and data['items']:
            snippet = data['items'][0]['snippet']
            title = snippet['title']
            statistics = data['items'][0]['statistics']
            views = statistics['viewCount']
            likes = statistics['likeCount']
            return title, views, likes
        else:
            return None, None, None

    def __str__(self):
        return self.title

class PLVideo(Video):
    def __init__(self, video_id, playlist_id):
        super().__init__(video_id)
        self.playlist_id = playlist_id