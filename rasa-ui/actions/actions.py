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
        url = "http://thingsboardhost:9090/api/plugins/telemetry/DEVICE/349ecb90-6f21-11ee-acb9-cf4e84cef63d/values/timeseries?keys=tempreture"
        payload = {}
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJzdWhhc2Rldm1hbmVtYWlsQGdtYWlsLmNvbSIsInVzZXJJZCI6ImZkNDE4NDMwLTZmMjAtMTFlZS1hY2I5LWNmNGU4NGNlZjYzZCIsInNjb3BlcyI6WyJURU5BTlRfQURNSU4iXSwic2Vzc2lvbklkIjoiNDY3Y2E4ZGMtZTRjNS00ZWVlLWE5ZDAtZGRmNjdkMWRmMTNjIiwiaXNzIjoidGhpbmdzYm9hcmQuaW8iLCJpYXQiOjE3MDIyNDk4MjMsImV4cCI6MTcwMjg1NDYyMywiZmlyc3ROYW1lIjoic3VoYXMiLCJsYXN0TmFtZSI6ImRldm1hbmUiLCJlbmFibGVkIjp0cnVlLCJpc1B1YmxpYyI6ZmFsc2UsInRlbmFudElkIjoiYmRlNTZjNzAtNmYyMC0xMWVlLWFjYjktY2Y0ZTg0Y2VmNjNkIiwiY3VzdG9tZXJJZCI6IjEzODE0MDAwLTFkZDItMTFiMi04MDgwLTgwODA4MDgwODA4MCJ9.vzrSDw9lXRD_AurFOhKbNztW1IkAN-hB6SPbRSimaU-mkw_mS6IAPko1yGkeY07qucySOHcyO1nS3dI8JqPivg'
        }
        response = requests.request(
            "GET", url, headers=headers, data=payload)
        print('status code:', response.status_code)
        print(response.text)
        temp = json.loads(response.text)["tempreture"][0]["value"]

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

        endpoint_url = "http://jena-fuski:3030/ds/sparql"
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
    


