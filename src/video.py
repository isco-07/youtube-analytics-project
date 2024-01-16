import os

from googleapiclient.discovery import build

api_key: str | None = os.getenv("YT_API_KEY")
youtube = build("youtube", "v3", developerKey=api_key)


class Video:
    def __init__(self, video_id):
        self.video_id = video_id
        video_response = (
            youtube.videos()
            .list(part="snippet,statistics,contentDetails,topicDetails", id=video_id)
            .execute()
        )
        try:
            self.title = video_response["items"][0]["snippet"]["title"]
        except IndexError:
            self.url = None
            self.title = None
            self.view_count = None
            self.like_count = None
        else:
            self.url = f"https://www.youtube.com/watch?v={self.video_id}"
            self.view_count = video_response["items"][0]["statistics"]["viewCount"]
            self.like_count = video_response["items"][0]["statistics"]["likeCount"]

    def __str__(self):
        return f"{self.title}"


class PLVideo(Video):
    def __init__(self, video_id, playlist_id):
        super().__init__(video_id)
        self.playlist_id = playlist_id
        video_response = (
            youtube.videos()
            .list(part="snippet,statistics,contentDetails,topicDetails", id=video_id)
            .execute()
        )
        self.url = f"https://www.youtube.com/watch?v={self.video_id}"
        self.title = video_response["items"][0]["snippet"]["title"]
        self.view_count = video_response["items"][0]["statistics"]["viewCount"]
        self.like_count = video_response["items"][0]["statistics"]["likeCount"]
