import os
import praw
import process_nlp
from dataclasses import dataclass
from datetime import datetime
from time import sleep
from geopy.geocoders import Nominatim

def main():
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
        username="praw-api-account",
        password="=)7sq+gCxU.=p2N",
        client_secret="hiAz-2dmaKkHtOw3NOsm5SlFv1Cb-w",
        client_id="bSL7WFed_benr2jpRsG1ug",
        user_agent="praw-service"
    )
    posts = [Post(x.title, x.url, x.created_utc, []) for x in instance.subreddit("worldnews").hot(limit=5)]
    process_nlp.parse_entities(posts)
    get_locations(posts)

    for post in posts:
        print(post.title)
        for l in post.locations:
            print(l.name, l.coordinates)

if __name__ == "__main__":
    main()