# actions.py
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

class CustomAction(Action):
    def name(self) -> Text:
        return "custom_action"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        # Get the user input
        user_input = tracker.latest_message.get("text", "")

        # Perform custom logic based on the user input
        # ...

        # Respond to the user
        dispatcher.utter_message("Action performed successfully!")

        return []
