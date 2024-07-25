# actions.py

import requests
import json
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
import psycopg2
from psycopg2.extras import DictCursor
import SPARQLWrapper
from SPARQLWrapper import SPARQLWrapper, JSON
from datetime import datetime
import time

class action_nl2sparql_jena(Action):
    def name(self) -> str:
        return "action_nl2sparql_jena"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: dict) -> list:
        
        # Step 1: Translate user query to SPARQL
        user_query = tracker.latest_message['text']
        translate_url = "http://localhost:5002/translate"
        endpoint_url = "http://localhost:3030/abacws-sensor-network/sparql"
        summarize_url = "http://localhost:5000/generate_explanation"
        headers = {"Content-Type": "application/json"}
        payload = {"query": user_query}

        try:
            response = requests.post(translate_url, headers=headers, json=payload)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            dispatcher.utter_message(text="Error: Unable to translate your question to machine understanding language. Please try again using different words.")
            return []

        sparql_query = response.json().get("sparql_query")
        if not sparql_query:
            dispatcher.utter_message(text="Error: Translation service did not return a SPARQL query. Please try again.")
            return []

        # Step 2: Execute SPARQL query
        final_sparql_query_template = """
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX bldg: <http://abacwsbuilding.cardiff.ac.uk/abacws#>
        PREFIX brick: <https://brickschema.org/schema/Brick#>
        PREFIX owl: <http://www.w3.org/2002/07/owl#>
        PREFIX sh: <http://www.w3.org/ns/shacl#>
        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
        PREFIX ref: <https://brickschema.org/schema/Brick/ref#>
        """
        final_sparql_query = final_sparql_query_template + sparql_query

        results = self.execute_sparql_query(final_sparql_query, endpoint_url)

        if not results:
            dispatcher.utter_message(text="No results found in database. Their is no data to show.")
            return []

        formatted_results = self.format_results(results, self.prefix_mappings())

        # Step 3: Summarize the sparql response in natural language
        data = {
            "en": user_query,
            "response": formatted_results
        }

        try:
            response = requests.post(summarize_url, json=data)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            dispatcher.utter_message(text=f"Failed to receive response. Status code: {response.status_code}")
            return []

        explanation = response.json().get('explanation', "No explanation available.")
        dispatcher.utter_message(text=f"{explanation}")

        return []

    def execute_sparql_query(self, sparql_query, endpoint_url):
        try:
            sparql = SPARQLWrapper(endpoint_url)
            sparql.setQuery(sparql_query)
            sparql.setReturnFormat(JSON)
            results = sparql.query().convert()
            return results["results"]["bindings"]
        except Exception as e:
            return []

    def prefix_mappings(self):
        return {
            "http://abacwsbuilding.cardiff.ac.uk/abacws#": "bldg:",
            "https://brickschema.org/schema/Brick#": "brick:",
            "http://www.w3.org/1999/02/22-rdf-syntax-ns#": "rdf:",
            "http://www.w3.org/2000/01/rdf-schema#": "rdfs:",
            "http://www.w3.org/2002/07/owl#": "owl:",
            "http://www.w3.org/ns/shacl#": "sh:",
            "http://www.w3.org/2001/XMLSchema#": "xsd:",
            "https://w3id.org/rec#": "rec",
            "https://brickschema.org/schema/Brick/ref#": "ref:"
        }

    def remove_prefix(self, uri, prefix_mappings):
        for prefix, replacement in prefix_mappings.items():
            if uri.startswith(prefix):
                return uri.replace(prefix, replacement)
        return uri

    def format_results(self, results_bindings, prefix_mappings):
        formatted_bindings = []
        for binding in results_bindings:
            formatted_binding = {var: self.remove_prefix(binding[var]['value'], prefix_mappings) for var in binding}
            formatted_bindings.append(formatted_binding)
        return formatted_bindings
    