from models import RedditPosts, Story, StoryLocation, Location
from geopy.geocoders import Nominatim
from time import sleep
from dataclasses import asdict
from datetime import datetime
from supabase import Client

def build_stories(posts: list[RedditPosts], supabase_client: Client):
    for post in posts:
        # Insert our story into supabase. There can be constraints with unique urls so some may fail
        data = []
        try:
            data, _ = supabase_client.table('stories').insert({"title":post.title, "url": post.url, "date_created": datetime.utcfromtimestamp(post.date_created).strftime('%Y-%m-%dT%H:%M:%SZ')}).execute()
        except:
            continue
        post_ref = data[1][0]
        if not data: 
            continue
        story_ref = Story(post_ref['id'],post_ref['title'],post_ref['date_created'],post_ref['url'])
        for l in post.locations:
            location_response = supabase_client.table('locations').select('*').eq('name', l).execute()
            print(location_response)
            # If we find a location, we want to use that for our story_location table
            if location_response.data:
                supabase_client.table('story_locations').insert({'location_id': location_response.data[0]['id'], 'story_id': post_ref['id']})
            else:
                # If we don't find it, we check our Geocoding API. We also want to rate limit this
                geolocator = Nominatim(user_agent="geostory")
                location = geolocator.geocode(l)
                insert_location_response = supabase_client.table('locations').insert({'name': l, 'coordinates': f'({location.latitude},{location.longitude})'}).execute()
                print(insert_location_response)
                print(post_ref['id'])
                supabase_client.table('story_locations').insert({'location_id': insert_location_response.data[0]['id'], 'story_id': post_ref['id']}).execute()
                sleep(1)

                
