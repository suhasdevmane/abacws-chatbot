# custom_actions/action_get_temperature.py
import requests
import json
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from typing import Any, Text, Dict, List
import subprocess
from SPARQLWrapper import SPARQLWrapper, JSON
import csv

class ActionGetTemperature(Action):
    def name(self) -> Text:
        return "action_asked_temperature"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        url = "http://mytb:8080/api/plugins/telemetry/DEVICE/478abf30-7db2-11ee-b0f3-69bd975277c1/values/timeseries?keys=Temperature"
        payload = {}
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'YourAuthorizationTokenHere'
        }

        response = requests.request("GET", url, headers=headers, data=payload)
        print('status code:', response.status_code)
        print(response.text)

        try:
            temp = json.loads(response.text)["Temperature"][0]["value"]
            dispatcher.utter_message(text="Temperature is {} degrees".format(temp))
        except (KeyError, IndexError):
            dispatcher.utter_message(text="Couldn't get current temperature. Please try again")

        return []
