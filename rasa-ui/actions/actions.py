from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import requests
import subprocess
from SPARQLWrapper import SPARQLWrapper, JSON
import json
import csv


class action_give_temp(Action):
    def name(self) -> Text:
        return "action_asked_temperature"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # ---------------------------
        url = "https://thingsboard.cs.cf.ac.uk/api/plugins/telemetry/DEVICE/fef50770-57f1-11ee-8714-19d56ba0c4fd/values/timeseries?keys=G"
        payload = {}
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJTdWhhc0FiYWN3c0xpdmluZ0xhYkBjYXJkaWZmLmFjLnVrIiwic2NvcGVzIjpbIlRFTkFOVF9BRE1JTiJdLCJ1c2VySWQiOiIzNTg1MzkzMC1kYjc2LTExZWMtOTY0NC0zZDY2MDFiMTlmMmMiLCJmaXJzdE5hbWUiOiJTdWhhcyIsImxhc3ROYW1lIjoiRGV2bWFuZSIsImVuYWJsZWQiOnRydWUsImlzUHVibGljIjpmYWxzZSwidGVuYW50SWQiOiJmOTFlNDU5MC1kYjc1LTExZWMtOTY0NC0zZDY2MDFiMTlmMmMiLCJjdXN0b21lcklkIjoiMTM4MTQwMDAtMWRkMi0xMWIyLTgwODAtODA4MDgwODA4MDgwIiwiaXNzIjoidGhpbmdzYm9hcmQuaW8iLCJpYXQiOjE2OTcxOTQyOTMsImV4cCI6MTY5NzIwMzI5M30.CEJRGkkEBvKTQw2XEc3u3O-L0a7D7NcpF3I4l9Q5VjJUoqYVEJRffWuu5AHvbmzYDg9EGu3Has8pkonWZaT5_A'
        }
        response = requests.request(
            "GET", url, headers=headers, data=payload)
        print('status code:', response.status_code)
        print(response.text)
        temp = json.loads(response.text)["G"][0]["value"]

        if not temp:
            dispatcher.utter_message(
                text="could'nt get current temperature. please try again")
        else:
            dispatcher.utter_message(
                text=" temperature is {} degrees".format(temp))
        return []


class action_give_report(Action):
    def name(self) -> Text:
        return "action_asked_report"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        endpoint_url = "http://localhost:3030/ds/sparql"
        sparql_query = """
            PREFIX brick: <https://brickschema.org/schema/Brick#>
            PREFIX brick1: <https://brickschema.org/schema/1.0.2/building_example#>
            SELECT * WHERE {
                brick1:ahu_A1 brick:feeds ?obj .
            } LIMIT 5
        """

        def execute_sparql_query(sparql_query, endpoint_url):
            sparql = SPARQLWrapper(endpoint_url)
            sparql.setQuery(sparql_query)
            sparql.setReturnFormat(JSON)
            results = sparql.query().convert()
            return results
        ans = execute_sparql_query(sparql_query, endpoint_url)
        headers = ans['head']['vars']
        data_rows = []
        for binding in ans['results']['bindings']:
            row = [binding.get(var, {}).get('value', '') for var in headers]
            data_rows.append(row)
        with open('output.csv', mode='w', newline='', encoding='utf-8') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(headers)
            csv_writer.writerows(data_rows)
        print('CSV file saved as: output.csv')

        dispatcher.utter_message(attachment="output.csv")
        return []


class action_asked_entities(Action):
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
