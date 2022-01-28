from typing import (
    List,
)
from enum import Enum
from pydantic import BaseModel


class Category(Enum):
    SONGS = "Songs"
    REQUESTS = "Requests"
    ARTISTS = "Artists"
    UNKNOWN = "Unknown"  # When type not support in enum


class Suggestion(BaseModel):
    category: Category
    name: str
    url: str


class TrackHTMLResult(BaseModel):
    id_: str
    title: str
    lyrics: List[str]  # List of parts
