from dataclasses import dataclass

@dataclass
class Location:
    id: str
    location_name: str
    coordinates: tuple[float, float]

@dataclass
class Story:
    id: str
    title: str
    date_created: str
    url: str

@dataclass 
class RedditPosts:
    title: str
    url: str
    date_created: str
    locations: list[str]

@dataclass
class StoryLocation:
    id: str
    location_id: str
    story_id: str