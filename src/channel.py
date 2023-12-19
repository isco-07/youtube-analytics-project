import json
import os
from typing import Any

from googleapiclient.discovery import build

api_key: str | None = os.getenv("YT_API_KEY")
youtube = build("youtube", "v3", developerKey=api_key)


class Channel:
    """Класс для ютуб-канала"""

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.__channel_id = channel_id
        channel = (
            youtube.channels()
            .list(id=self.__channel_id, part="snippet,statistics")
            .execute()
        )
        self.title = channel["items"][0]["snippet"]["title"]
        self.channel_desc = channel["items"][0]["snippet"]["description"]
        self.video_count = channel["items"][0]["statistics"]["videoCount"]
        self.subscriber_count = channel["items"][0]["statistics"]["subscriberCount"]
        self.view_count = channel["items"][0]["statistics"]["viewCount"]
        self.url = f"https://www.youtube.com/channel/{channel_id}"

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        channel = (
            youtube.channels()
            .list(id=self.__channel_id, part="snippet,statistics")
            .execute()
        )
        print(json.dumps(channel, indent=2, ensure_ascii=False))

    @property
    def channel_id(self) -> str:
        """Возвращает __channel_id"""
        return self.__channel_id

    @staticmethod
    def get_service() -> Any:
        """Возвращает объект для работы с YouTube API"""
        return youtube

    def to_json(self, file_name: str) -> None:
        """Сохраняет в файл значения атрибутов экземпляра Channel"""
        with open(file_name, "w", encoding="utf-8") as f:
            obj_list = {
                "id": self.__channel_id,
                "nameChannel": self.title,
                "description": self.channel_desc,
                "url": self.url,
                "subscribers": self.subscriber_count,
                "videoCount": self.video_count,
                "viewCount": self.view_count,
            }
            f.write(json.dumps(obj_list, indent=2, ensure_ascii=False))
