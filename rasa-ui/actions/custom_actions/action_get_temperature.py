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
        url = "http://192.168.1.85:8080/api/plugins/telemetry/DEVICE/478abf30-7db2-11ee-b0f3-69bd975277c1/values/timeseries?keys=Temperature"
        payload = {}
        headers = {
            'Content-Type': 'application/json',
            "X-Authorization": "Bearer eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJzdWhhc2Rldm1hbmVtYWlsQGdtYWlsLmNvbSIsInVzZXJJZCI6ImZkNDE4NDMwLTZmMjAtMTFlZS1hY2I5LWNmNGU4NGNlZjYzZCIsInNjb3BlcyI6WyJURU5BTlRfQURNSU4iXSwic2Vzc2lvbklkIjoiNDY3Y2E4ZGMtZTRjNS00ZWVlLWE5ZDAtZGRmNjdkMWRmMTNjIiwiaXNzIjoidGhpbmdzYm9hcmQuaW8iLCJpYXQiOjE3MDIyNDk4MjMsImV4cCI6MTcwMjg1NDYyMywiZmlyc3ROYW1lIjoic3VoYXMiLCJsYXN0TmFtZSI6ImRldm1hbmUiLCJlbmFibGVkIjp0cnVlLCJpc1B1YmxpYyI6ZmFsc2UsInRlbmFudElkIjoiYmRlNTZjNzAtNmYyMC0xMWVlLWFjYjktY2Y0ZTg0Y2VmNjNkIiwiY3VzdG9tZXJJZCI6IjEzODE0MDAwLTFkZDItMTFiMi04MDgwLTgwODA4MDgwODA4MCJ9.vzrSDw9lXRD_AurFOhKbNztW1IkAN-hB6SPbRSimaU-mkw_mS6IAPko1yGkeY07qucySOHcyO1nS3dI8JqPivg",
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

