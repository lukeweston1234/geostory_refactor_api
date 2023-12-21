import os
import praw
from models import RedditPosts

def get_posts():
    instance = praw.Reddit(
        username=os.getenv('USERNAME'),
        password=os.getenv('PASSWORD'),
        client_secret=os.getenv('CLIENT_SECRET'),
        client_id=os.getenv('CLIENT_ID'),
        user_agent=os.getenv('USER_AGENT')
    )
    return [RedditPosts(x.title, x.url, x.created_utc, []) for x in instance.subreddit("worldnews").hot(limit=5) if not x.stickied]
   