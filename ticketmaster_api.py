import os
from os.path import join, dirname
from dotenv import load_dotenv
import requests

# set up spotify keys
dotenv_path = join(dirname(__file__), 'ticketmaster.env')
load_dotenv(dotenv_path)

TICKETMASTER_API_KEY = os.environ['TICKETMASTER_API_KEY']

def search_events(zipcode, artist, page):
    url = ("https://app.ticketmaster.com/discovery/v2/events.json?classificationName=music"
     + "&keyword=" + artist   
     + "&postalCode=" + zipcode
    + "&size=5&page="+page
    +"&apikey=" + TICKETMASTER_API_KEY 
    )
    
    response = requests.get(url, headers={    
        "Accept": "application/json",
        "Content-Type": "application/json",}
    )
    
    # if api response error
    if response.status_code != 200 or response.json()["page"]["totalElements"] == 0:
        return None
        
    event_details = parse_events(response.json())
    
    return response.json()
    
    
def parse_events(events_json):
    events = events_json["_embedded"]["events"]
    a = []
    for e in events:
        name = e["name"]
        print(name)
        url = e["url"]
        print(url)
        images = e["images"][0]["url"]
        print(images)
        date = e["dates"]["start"]["dateTime"]
        print(date)
        venue = e["_embedded"]["venues"][0]["name"]
        print(venue)
        a.append([name, url, images, date, venue])
        print(a)
    return events