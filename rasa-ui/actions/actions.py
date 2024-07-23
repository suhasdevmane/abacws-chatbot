<<<<<<< HEAD
<<<<<<< HEAD
=======
>>>>>>> bbb81bcf48433c9e82d368a909b444e50e73a165
# actions.py

import requests
import json
<<<<<<< HEAD
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
import psycopg2
from psycopg2.extras import DictCursor
from datetime import datetime
import time
import SPARQLWrapper
from SPARQLWrapper import SPARQLWrapper, JSON
from datetime import datetime
import time

class ActionQueryHandler(Action):
    def name(self) -> str:
        return "action_query_handler"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: dict) -> list:
        
        # Step 1: Translate user query to SPARQL
        user_query = tracker.latest_message['text']
        translate_url = "http://localhost:5002/translate"
        headers = {"Content-Type": "application/json"}
        payload = {"query": user_query}

        response = requests.post(translate_url, headers=headers, json=payload)

        if response.status_code != 200 or not response.json().get("sparql_query"):
            dispatcher.utter_message(text="Error: Unable to translate the query to SPARQL.")
            return []

        sparql_query = response.json().get("sparql_query")

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

        endpoint_url = "http://localhost:3030/abacws-sensor-network/sparql"
        results = self.execute_sparql_query(final_sparql_query, endpoint_url)

        if not results:
            dispatcher.utter_message(text="No results found.")
            return []

        formatted_results = self.format_results(results, self.prefix_mappings())

        # Step 3: Query PostgreSQL and calculate the average temperature
        conn_params = {
            'database': 'thingsboard',
            'user': 'thingsboard',
            'password': 'postgres',
            'host': 'localhost',
            'port': 5432,
        }

        start_date = tracker.get_slot("start_date")
        end_date = tracker.get_slot("end_date")
        start_date_unix = int(time.mktime(datetime.strptime(start_date, "%d/%m/%Y %H:%M:%S").timetuple()) * 1000)
        end_date_unix = int(time.mktime(datetime.strptime(end_date, "%d/%m/%Y %H:%M:%S").timetuple()) * 1000)

        try:
            conn = psycopg2.connect(**conn_params)
            cur = conn.cursor(cursor_factory=DictCursor)

            total_value = 0
            count = 0

            for result in formatted_results:
                entity_id = result['timeseries_id']
                key = result['timeseries_key_id']
                
                sql_query = """
                SELECT AVG(COALESCE(bool_v::TEXT, str_v, long_v::TEXT, dbl_v::TEXT, json_v::TEXT)::numeric) AS average_value
                FROM ts_kv
                WHERE entity_id = %s AND key = %s AND ts BETWEEN %s AND %s;
                """
                cur.execute(sql_query, (entity_id, key, start_date_unix, end_date_unix))
                
                sql_result = cur.fetchone()
                if sql_result and sql_result[0] is not None:
                    total_value += sql_result[0]
                    count += 1

            overall_average = total_value / count if count > 0 else None

        except Exception as e:
            dispatcher.utter_message(text=f"An error occurred: {e}")
            return []

        finally:
            if cur:
                cur.close()
            if conn:
                conn.close()

        # Step 4: Summarize the response
        if overall_average is None:
            dispatcher.utter_message(text="Could not calculate the average temperature.")
            return []

        summarize_url = "http://localhost:5000/generate_explanation"
        data = {
            "en": "What is the average temperature?",
            "response": f"Overall average temperature: {overall_average}"
        }

        response = requests.post(summarize_url, json=data)

        if response.status_code == 200:
            explanation = response.json().get('explanation')
            dispatcher.utter_message(text=f"Explanation: {explanation}")
        else:
            dispatcher.utter_message(text=f"Failed to receive response. Status code: {response.status_code}")

        return []

    def execute_sparql_query(self, sparql_query, endpoint_url):
        sparql = SPARQLWrapper(endpoint_url)
        sparql.setQuery(sparql_query)
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        return results

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
=======
from typing import Any, Text, Dict, List
=======
>>>>>>> bbb81bcf48433c9e82d368a909b444e50e73a165
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
import psycopg2
from psycopg2.extras import DictCursor
from datetime import datetime
import time
import SPARQLWrapper
from SPARQLWrapper import SPARQLWrapper, JSON
from datetime import datetime
import time

class ActionQueryHandler(Action):
    def name(self) -> str:
        return "action_query_handler"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: dict) -> list:
        
        # Step 1: Translate user query to SPARQL
        user_query = tracker.latest_message['text']
        translate_url = "http://localhost:5002/translate"
        headers = {"Content-Type": "application/json"}
        payload = {"query": user_query}

        response = requests.post(translate_url, headers=headers, json=payload)

        if response.status_code != 200 or not response.json().get("sparql_query"):
            dispatcher.utter_message(text="Error: Unable to translate the query to SPARQL.")
            return []

        sparql_query = response.json().get("sparql_query")

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

<<<<<<< HEAD
>>>>>>> d43c0ebbd314716768d4380424349e8f915e277e
=======
        endpoint_url = "http://localhost:3030/abacws-sensor-network/sparql"
        results = self.execute_sparql_query(final_sparql_query, endpoint_url)

        if not results:
            dispatcher.utter_message(text="No results found.")
            return []

        formatted_results = self.format_results(results, self.prefix_mappings())

        # Step 3: Query PostgreSQL and calculate the average temperature
        conn_params = {
            'database': 'thingsboard',
            'user': 'thingsboard',
            'password': 'postgres',
            'host': 'localhost',
            'port': 5432,
        }

        start_date = tracker.get_slot("start_date")
        end_date = tracker.get_slot("end_date")
        start_date_unix = int(time.mktime(datetime.strptime(start_date, "%d/%m/%Y %H:%M:%S").timetuple()) * 1000)
        end_date_unix = int(time.mktime(datetime.strptime(end_date, "%d/%m/%Y %H:%M:%S").timetuple()) * 1000)

        try:
            conn = psycopg2.connect(**conn_params)
            cur = conn.cursor(cursor_factory=DictCursor)

            total_value = 0
            count = 0

            for result in formatted_results:
                entity_id = result['timeseries_id']
                key = result['timeseries_key_id']
                
                sql_query = """
                SELECT AVG(COALESCE(bool_v::TEXT, str_v, long_v::TEXT, dbl_v::TEXT, json_v::TEXT)::numeric) AS average_value
                FROM ts_kv
                WHERE entity_id = %s AND key = %s AND ts BETWEEN %s AND %s;
                """
                cur.execute(sql_query, (entity_id, key, start_date_unix, end_date_unix))
                
                sql_result = cur.fetchone()
                if sql_result and sql_result[0] is not None:
                    total_value += sql_result[0]
                    count += 1

            overall_average = total_value / count if count > 0 else None

        except Exception as e:
            dispatcher.utter_message(text=f"An error occurred: {e}")
            return []

        finally:
            if cur:
                cur.close()
            if conn:
                conn.close()

        # Step 4: Summarize the response
        if overall_average is None:
            dispatcher.utter_message(text="Could not calculate the average temperature.")
            return []

        summarize_url = "http://localhost:5000/generate_explanation"
        data = {
            "en": "What is the average temperature?",
            "response": f"Overall average temperature: {overall_average}"
        }

        response = requests.post(summarize_url, json=data)

        if response.status_code == 200:
            explanation = response.json().get('explanation')
            dispatcher.utter_message(text=f"Explanation: {explanation}")
        else:
            dispatcher.utter_message(text=f"Failed to receive response. Status code: {response.status_code}")

        return []

    def execute_sparql_query(self, sparql_query, endpoint_url):
        sparql = SPARQLWrapper(endpoint_url)
        sparql.setQuery(sparql_query)
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        return results

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
>>>>>>> bbb81bcf48433c9e82d368a909b444e50e73a165
