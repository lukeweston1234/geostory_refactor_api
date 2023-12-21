import os
import praw
import process_nlp
from dataclasses import dataclass
from datetime import datetime
from time import sleep
from geopy.geocoders import Nominatim
from dotenv import load_dotenv



def main():
    load_dotenv()
    get_posts()

@dataclass 
class Location:
    name: str
    coordinates: tuple[float, float] = (0,0)

@dataclass
class Post:
    title: str
    url: str
    date: str
    locations: list[Location]

def get_locations(posts: list[Post]):
    geolocator = Nominatim(user_agent="geostory")
    for p in posts:
        for l in p.locations:
            location = geolocator.geocode(l.name)
            l.coordinates = (location.latitude, location.longitude)
        sleep(1.5) # Rate limit for GeoCoding API

def get_posts():
    instance = praw.Reddit(
        username=os.getenv('username'),
        password=os.getenv('password'),
        client_secret=os.getenv('client_secret'),
        client_id=os.getenv('client_id'),
        user_agent=os.getenv('user_agent')
    )
    posts = [Post(x.title, x.url, x.created_utc, []) for x in instance.subreddit("worldnews").hot(limit=5) if not x.stickied]
    process_nlp.parse_entities(posts)
    get_locations(posts)

    for post in posts:
        print(post.title)
        for l in post.locations:
            print(l.name, l.coordinates)

if __name__ == "__main__":
    main()