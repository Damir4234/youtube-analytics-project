import datetime
import requests
import os


class PlayList:
    def __init__(self, playlist_id):
        self.playlist_id = playlist_id
        self.title = self.get_playlist_title()
        self.url = f"https://www.youtube.com/playlist?list={playlist_id}"

    @property
    def total_duration(self):

        response = requests.get(
            f"https://www.googleapis.com/youtube/v3/playlistItems?part=contentDetails&maxResults=50&playlistId={self.playlist_id}&key={os.getenv('api_you')}")
        data = response.json()

        total_seconds = 0
        for item in data['items']:
            video_id = item['contentDetails']['videoId']
            video_duration = self._get_video_duration(video_id)
            total_seconds += video_duration

        return datetime.timedelta(seconds=total_seconds)

    def _get_video_likes(self, video_id):
        response = requests.get(
            f"https://www.googleapis.com/youtube/v3/videos?part=statistics&id={video_id}&key={os.getenv('api_you')}")
        data = response.json()
        likes = data['items'][0]['statistics']['likeCount']
        return int(likes)

    def show_best_video(self):
        # Получение информации о видеозаписях в плейлисте
        response = requests.get(
            f"https://www.googleapis.com/youtube/v3/playlistItems?part=contentDetails&maxResults=50&playlistId={self.playlist_id}&key={os.getenv('api_you')}")
        data = response.json()

        best_video = None
        max_likes = 0
        for item in data['items']:
            video_id = item['contentDetails']['videoId']
            video_likes = self._get_video_likes(video_id)
            if video_likes > max_likes:
                max_likes = video_likes
                best_video = video_id

        return f"https://youtu.be/{best_video}"

    def get_playlist_title(self):
        response = requests.get(
            f"https://www.googleapis.com/youtube/v3/playlists?part=snippet&id={self.playlist_id}&key={os.getenv('api_you')}")
        data = response.json()
        return data['items'][0]['snippet']['title']

    def _get_video_duration(self, video_id):
        response = requests.get(
            f"https://www.googleapis.com/youtube/v3/videos?part=contentDetails&id={video_id}&key={os.getenv('api_you')}")
        data = response.json()
        duration = data['items'][0]['contentDetails']['duration']
        return self._duration_to_seconds(duration)

    def _duration_to_seconds(self, duration_str):
        time_parts = duration_str.split('T')[1]
        hours, minutes, seconds = 0, 0, 0

        if 'H' in time_parts:
            hours = int(time_parts.split('H')[0])
            time_parts = time_parts.split('H')[1]

        if 'M' in time_parts:
            minutes = int(time_parts.split('M')[0])
            time_parts = time_parts.split('M')[1]

        if 'S' in time_parts:
            seconds = int(time_parts.split('S')[0])

        return hours * 3600 + minutes * 60 + seconds
