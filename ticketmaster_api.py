"""
Ticketmaster API and Parser
"""
import os
from os.path import join, dirname
from datetime import datetime
from dotenv import load_dotenv
import requests

# set up spotify keys
dotenv_path = join(dirname(__file__), "ticketmaster.env")
load_dotenv(dotenv_path)

TICKETMASTER_API_KEY = os.environ["TICKETMASTER_API_KEY"]


def search_events(zipcode, artist, page):
    """
    Request a response from Ticketmaster API
    """
    url = (
        "https://app.ticketmaster.com/discovery/v2/events.json?classificationName=music"
        + "&keyword="
        + artist
        + "&postalCode="
        + zipcode
        + "&size=5&page="
        + page
        + "&apikey="
        + TICKETMASTER_API_KEY
    )

    response = requests.get(
        url, headers={"Accept": "application/json", "Content-Type": "application/json"}
    )
    # if api response error
    if response.status_code != 200:
        return None

    response_json = response.json()
    if response_json["page"]["totalElements"] == 0:
        return None

    event_details = parse_events(response_json)

    return event_details


def parse_events(events_json):
    """
    Parse and return list of events
    """
    events = events_json["_embedded"]["events"]
    num_pages = events_json["page"]["totalPages"]
    curr_page = events_json["page"]["number"]
    all_events = []
    for e in events:
        name = e["name"]
        url = e["url"]
        images = e["images"][0]["url"]
        try:
            date = datetime.strptime(e["dates"]["start"]["dateTime"], "%Y-%m-%dT%XZ")
            date = date.strftime("%B %d, %Y")
        except KeyError:
            date = "To be announced"
        try:
            venue = e["_embedded"]["venues"][0]["name"]
        except KeyError:
            venue = "To be announced"
        all_events.append(
            {
                "name": name,
                "url": url,
                "image": images,
                "date": date,
                "venue": venue,
                "totalPages": num_pages,
                "currPage": curr_page,
            }
        )
    return all_events
