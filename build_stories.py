from models import RedditPosts, Story
from geopy.geocoders import Nominatim
from time import sleep
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
        if not post_ref: 
            continue
        story_ref = Story(post_ref['id'],post_ref['title'],post_ref['date_created'],post_ref['url'])
        for l in post.locations:
            location_response = supabase_client.table('locations').select('*').eq('name', l).execute()
            # If we find a location, we want to use that for our story_location table
            if location_response.data:
                supabase_client.table('story_locations').insert({'location_id': location_response.data[0]['id'], 'story_id': post_ref['id']}).execute()
            else:
                # If we don't find it, we check our Geocoding API. We also want to rate limit this
                geolocator = Nominatim(user_agent="geostory")
                location = geolocator.geocode(l)
                # We don't want duplicate locations for duplicate coordinates, i.e United States and United States of America.
                # The insert can throw if it already exists, if it does, we will double check for an existing location
                # If that location exists, we will just reference that one
                location_id = None
                try:
                    insert_location_response = supabase_client.table('locations').insert({'name': l, 'x_coordinate': location.longitude, 'y_coordinate': location.latitude}).execute()
                    location_id = insert_location_response.data[0]['id']
                except:
                    insert_location_response = supabase_client.table('locations').select("id").eq('x_coordinate', location.longitude).eq('y_coordinate', location.latitude).execute()
                    location_id = insert_location_response.data[0]['id']
                if (location_id):
                    try:
                        supabase_client.table('story_locations').insert({'location_id': location_id, 'story_id': post_ref['id']}).execute()
                        sleep(1)
                    except: 
                        continue


                
