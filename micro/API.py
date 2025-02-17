from discord import Webhook
from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime

from classes import CEmbed
from static.constants import EVENTS_ROLE_ID

import os, aiohttp

class Event(BaseModel):
    title: str
    image: str
    date_time: str
    duration: int
    short_description: str
    event_link: str
    event_location: str
    seats: int
    mentions: list[int]


app = FastAPI()


def get_embed(event: Event):
    date_time = event.date_time.split()
    date = datetime.strptime(date_time[0], "%Y-%m-%d")
    time = datetime.strptime(date_time[1], "%H:%M")
    return CEmbed.from_dict(
        {
            "title": event.title,
            "image": {'url': event.image},
            "fields": [
                {
                    "name": "Description", 
                    "value": event.short_description
                },

                {
                    "name": "Date",
                    "value": date.strftime("%Y-%m-%d"), 
                    "inline": True
                },
                {
                    "name": "Time",
                    "value": time.strftime("%H:%M"),
                    "inline": True
                },
                {
                    "name": "Duration",
                    "value": event.duration,
                    "inline": True
                },
                {
                    "name": "Link",
                    "value": f"[Click Here]({event.event_link})",
                    "inline": True
                },
                {
                    "name": "Event Location",
                    "value": event.event_location,
                    "inline": True
                },
                {
                    "name": "Seats",
                    "value": event.seats,
                    "inline": True
                },
            ],
        }
    )


@app.post("/bot/event")
async def publish_event(event: Event):
    WB_URL = os.getenv("WEBHOOK_URL")

    async with aiohttp.ClientSession() as session:
        mentions = " ".join([f"<@&{id}>" for id in event.mentions])
        webhook = Webhook.from_url(WB_URL, session=session)
        await webhook.send(content=f"<@&{EVENTS_ROLE_ID}>{mentions}", embed=get_embed(event))
