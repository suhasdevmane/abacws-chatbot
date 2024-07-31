import requests
import json
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
from SPARQLWrapper import SPARQLWrapper, JSON
from datetime import datetime
import logging

class action_nl2sparql_jena(Action):
    def name(self) -> str:
        return "action_nl2sparql_jena"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # Step 1: Translate user query to SPARQL
        user_query = tracker.latest_message['text']
        logging.debug(f"user query is: {user_query}")
        translate_url = "http://t5-t5:5000/translate"
        endpoint_url = "http://jena-fuseki:3030/abacws-sensor-network/sparql"
        summarize_url = "http://t5-t5:5000/summarize"
        headers = {"Content-Type": "application/json"}
        payload = {"query": user_query}

        try:
            response = requests.post(translate_url, headers=headers, json=payload)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            dispatcher.utter_message(text="Error: Unable to translate your question to machine understanding language. Please try again using different words.")
            logging.error(f"Error during translation: {e}")
            return []

        sparql_query = response.json().get("sparql_query")
        logging.debug(f"sparql query received: {sparql_query}")
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
        if sparql_query:
            final_sparql_query = final_sparql_query_template + sparql_query
        else:
            final_sparql_query = None

        # Execute the SPARQL query
        if final_sparql_query:
            results = self.execute_sparql_query(final_sparql_query, endpoint_url)
            logging.debug(f"result received from SPARQL endpoint")
        else:
            logging.error("Error: No SPARQL query to execute.")
            return []

        if not results:
            dispatcher.utter_message(text="No results found in the database. There is no data to show.")
            return []

        results_bindings = results.get("results", {}).get("bindings", [])
        if results_bindings:
            formatted_results = self.format_results(results_bindings, self.prefix_mappings())
            logging.debug("Formatted Results:")
            logging.debug(formatted_results)
        else:
            dispatcher.utter_message(text="No results found.")
            return []

        # Step 3: Summarize the SPARQL response in natural language
        formatted_results_cleaned = formatted_results.replace('\n', ' ').replace('{', '').replace('}', '')
        data = user_query + " " + formatted_results_cleaned
        logging.debug(f"data sending to the summarization: {data}")
        headers1 = {"Content-Type": "text/plain"}
        try:
            response = requests.post(summarize_url, headers=headers1, data=data)
            response.raise_for_status()

            # Check if response is JSON
            try:
                # explanation = response.json().get('explanation', "No explanation available.")
                explanation = response.text
            except json.JSONDecodeError:
                logging.error(f"Failed to decode JSON from response: {response.text}")
                dispatcher.utter_message(text="Failed to decode the summary response.")
                return []

            dispatcher.utter_message(text=f"{explanation}")

        except requests.exceptions.RequestException as e:
            logging.error(f"Error during summarization: {str(e)}")
            if response is not None:
                logging.error(f"Response content: {response.text}")  # Log response content for debugging
            dispatcher.utter_message(text="Failed to receive response from summarization. Please try again later.")
            return []

        return []

    def execute_sparql_query(self, sparql_query, endpoint_url):
        try:
            sparql = SPARQLWrapper(endpoint_url)
            sparql.setQuery(sparql_query)
            sparql.setReturnFormat(JSON)
            results = sparql.query().convert()
            return results
        except Exception as e:
            logging.error(f"Error executing SPARQL query: {e}")
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
            "https://w3id.org/rec#": "rec:",
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
            formatted_bindings.append(", ".join(f"{var}: {formatted_binding[var]}" for var in formatted_binding))
        return ", ".join(formatted_bindings)
