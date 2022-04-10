import os
import requests


# Sending a post request to the app that will publish an SSE
def send_event(data):
    requests.post(os.environ["EVENTS_URL"],
                  json=data,
                  params={ "key": os.environ["WORKER_SECRET"] })