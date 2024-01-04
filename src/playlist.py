import os
from datetime import timedelta

import isodate
from googleapiclient.discovery import build

api_key: str | None = os.getenv("YT_API_KEY")
youtube = build("youtube", "v3", developerKey=api_key)


class PlayList:
    def __init__(self, playlist_id):
        channel_id = (
            youtube.playlistItems()
            .list(
                playlistId=playlist_id,
                part="snippet",
                maxResults=50,
            )
            .execute()["items"][0]["snippet"]["channelId"]
        )
        playlists = (
            youtube.playlists()
            .list(
                channelId=channel_id,
                part="contentDetails,snippet",
                maxResults=50,
            )
            .execute()
        )
        for playlist in playlists["items"]:
            if playlist["id"] == playlist_id:
                self.title = playlist["snippet"]["title"]
                self.url = f"https://www.youtube.com/playlist?list={playlist_id}"
                self.__playlist_id = playlist_id
                self.__playlist_videos = (
                    youtube.playlistItems()
                    .list(
                        playlistId=self.__playlist_id,
                        part="contentDetails",
                        maxResults=50,
                    )
                    .execute()
                )
                break

    @property
    def total_duration(self):
        video_ids: list[str] = [
            video["contentDetails"]["videoId"]
            for video in self.__playlist_videos["items"]
        ]
        video_response = (
            youtube.videos()
            .list(part="contentDetails,statistics", id=",".join(video_ids))
            .execute()
        )
        return sum(
            [
                isodate.parse_duration(video["contentDetails"]["duration"])
                for video in video_response["items"]
            ],
            timedelta(),
        )

    def show_best_video(self):
        playlist_videos = (
            youtube.playlistItems()
            .list(
                playlistId=self.__playlist_id,
                part="contentDetails",
                maxResults=50,
            )
            .execute()
        )
        video_ids: list[str] = [
            video["contentDetails"]["videoId"] for video in playlist_videos["items"]
        ]
        video_statistics = []
        for video_id in video_ids:
            video_statistics.append(
                youtube.videos().list(part="statistics", id=video_id).execute()
            )
        return (
            f"https://youtu.be/"
            f"{max(video_statistics, key=lambda x: x['items'][0]['statistics']['likeCount'])['items'][0]['id']}"
        )
