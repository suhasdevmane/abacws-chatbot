# custom_actions/action_give_report.py
import csv
import json
import requests
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from SPARQLWrapper import SPARQLWrapper, JSON
from typing import Any, Text, Dict, List

class ActionGiveReport(Action):
    def name(self) -> Text:
        return "action_asked_report"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        endpoint_url = "http://jena-fuski:3030/ds/sparql"
        sparql_query = """
            PREFIX brick: <https://brickschema.org/schema/Brick#>
            PREFIX ref: <http://example.org/reference#>
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
            SELECT uuid, ts, key
            FROM ts_kv
            WHERE entity_id = 'b4f415d0-7db2-11ee-b0f3-69bd975277c1'
            LIMIT 5;
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