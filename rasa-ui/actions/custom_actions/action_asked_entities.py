from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import requests
import subprocess
from SPARQLWrapper import SPARQLWrapper, JSON
import json
import csv



class ActionAskedEntities(Action):
    def name(self) -> Text:
        return "action_asked_entities"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        ent = tracker.latest_message['entities']
        dispatcher.utter_message(
            text=("your entities are: ")
        )
        dispatcher.utter_message(
            text=(ent)
        )

        return []