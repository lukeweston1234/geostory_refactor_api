import os
import process_nlp
from models import Location, Story, StoryLocation
from datetime import datetime
from reddit_api import get_posts
from dotenv import load_dotenv
from build_stories import build_stories
from process_nlp import parse_entities
from supabase import create_client, Client

def main():
    load_dotenv()
    url: str = os.environ.get("SUPABASE_URL")
    key: str = os.environ.get("SUPABASE_KEY")
    supabase_client: Client = create_client(url, key)
    posts = get_posts()
    parse_entities(posts)
    build_stories(posts, supabase_client)

if __name__ == "__main__":
    main()