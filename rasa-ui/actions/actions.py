from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import requests
import subprocess
from SPARQLWrapper import SPARQLWrapper, JSON
import json
import csv
import psycopg2
from psycopg2.extras import DictCursor
from datetime import datetime


class action_give_temp(Action):
    def name(self) -> Text:
        return "action_asked_temperature"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # ---------------------------
        url = "http://192.168.1.85:8080/api/plugins/telemetry/DEVICE/478abf30-7db2-11ee-b0f3-69bd975277c1/values/timeseries?keys=tempreture"
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


# class action_asked_entities(Action):
#     def name(self) -> Text:
#         return "action_asked_entities"

#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#         ent = tracker.latest_message['entities']
#         dispatcher.utter_message(
#             text=("your entities are: ")
#         )
#         dispatcher.utter_message(
#             text=(ent)
#         )

#         return []
    

    # =============



class query_sql_node_sensor(Action):
    def name(self) -> Text:
        return "query_sql_node_sensor"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
            sensor_node_entity = next(tracker.get_latest_entity_values("sensor_nodes"), None)
            data_to_fetch_entity = next(tracker.get_latest_entity_values("data_to_fetch"), None)
            if not sensor_node_entity or not data_to_fetch_entity:
                 dispatcher.utter_message(text="Please provide a valid sensor node and data to fetch.")
                 return []

            device_name_variable = sensor_node_entity
            user_input_key = data_to_fetch_entity
    
            sensor_nodes = [
                "node_5.01",
                "node_5.02",
                "node_5.03",
                "node_5.04",
                "node_5.05",
                "node_5.06",
                "node_5.07",
                "node_5.08",
                "node_5.09",
                "node_5.10",
                "node_5.11",
                "node_5.12",
                "node_5.13",
                "node_5.14",
                "node_5.15",
                "node_5.16",
                "node_5.17",
                "node_5.18",
                "node_5.19",
                "node_5.20",
                "node_5.21",
                "node_5.22",
                "node_5.23",
                "node_5.24",
                "node_5.25",
                "node_5.26",
                "node_5.27",
                "node_5.28",
                "node_5.29",
                "node_5.30",
                "node_5.31",
                "node_5.32",
                "node_5.33",
                "node_5.34",
            ]

            data_to_fetch = [
                "airQualityValue",
                "c2h5ch",
                "co_gas",
                "co2value",
                "PM10Atmospheric",
                "hchoppmvalue",
                "humidity",
                "lux",
                "rsroratio5",
                "rsroratio9",
                "rsroratio3",
                "rsroratio2",
                "NO2",
                "o2per",
                "memsvalue",
                "tempreture",
                "VOC",
            ]

            connection1 = psycopg2.connect(
                database="thingsboard",
                user="thingsboard",
                password="postgres",
                host="192.168.1.85",
                port=5432,
            )
            cursor1 = connection1.cursor(cursor_factory=DictCursor)
            query1 = f"""
            SELECT key_id FROM ts_kv_dictionary
            WHERE key = '{user_input_key}';
            """
            cursor1.execute(query1)
            rows1 = cursor1.fetchall()
            key_id_result = rows1[0]["key_id"] if rows1 else None
            # print("Key ID:", key_id_result)
            cursor1.close()
            # Mapping dictionary for device_name to entity_id
            device_name_to_entity_id = {
                "node_5.01": "478abf30-7db2-11ee-b0f3-69bd975277c1",
                "node_5.02": "5306a860-7db2-11ee-b0f3-69bd975277c1",
                "node_5.03": "6b52c020-7db2-11ee-b0f3-69bd975277c1",
                "node_5.04": "725a3830-7db2-11ee-b0f3-69bd975277c1",
                "node_5.05": "78df12c0-7db2-11ee-b0f3-69bd975277c1",
                "node_5.06": "8084c6a0-7db2-11ee-b0f3-69bd975277c1",
                "node_5.07": "8c34df30-7db2-11ee-b0f3-69bd975277c1",
                "node_5.08": "93834b50-7db2-11ee-b0f3-69bd975277c1",
                "node_5.09": "997b9d50-7db2-11ee-b0f3-69bd975277c1",
                "node_5.10": "9f44f010-7db2-11ee-b0f3-69bd975277c1",
                "node_5.11": "a6250a00-7db2-11ee-b0f3-69bd975277c1",
                "node_5.12": "add0b150-7db2-11ee-b0f3-69bd975277c1",
                "node_5.13": "b4f415d0-7db2-11ee-b0f3-69bd975277c1",
                "node_5.14": "bad9ca30-7db2-11ee-b0f3-69bd975277c1",
                "node_5.15": "c0fe3540-7db2-11ee-b0f3-69bd975277c1",
                "node_5.16": "729855d0-7db6-11ee-b0f3-69bd975277c1",
                "node_5.17": "328afde0-83f5-11ee-a992-8978af4232d8",
                "node_5.18": "37c9eaf0-83f5-11ee-a992-8978af4232d8",
                "node_5.19": "3d369ec0-83f5-11ee-a992-8978af4232d8",
                "node_5.20": "4e709010-83f5-11ee-a992-8978af4232d8",
                "node_5.21": "53491a30-83f5-11ee-a992-8978af4232d8",
                "node_5.22": "58b83f00-83f5-11ee-a992-8978af4232d8",
                "node_5.23": "5d800040-83f5-11ee-a992-8978af4232d8",
                "node_5.24": "620958f0-83f5-11ee-a992-8978af4232d8",
                "node_5.25": "6694ad70-83f5-11ee-a992-8978af4232d8",
                "node_5.26": "6b6a7870-83f5-11ee-a992-8978af4232d8",
                "node_5.27": "7091e5e0-83f5-11ee-a992-8978af4232d8",
                "node_5.28": "759e7850-83f5-11ee-a992-8978af4232d8",
                "node_5.29": "7b537fc0-83f5-11ee-a992-8978af4232d8",
                "node_5.30": "7ffd58c0-83f5-11ee-a992-8978af4232d8",
                "node_5.31": "84bd51d0-83f5-11ee-a992-8978af4232d8",
                "node_5.32": "8afd3420-83f5-11ee-a992-8978af4232d8",
                "node_5.33": "90088e10-83f5-11ee-a992-8978af4232d8",
                "node_5.34": "9586a700-83f5-11ee-a992-8978af4232d8"
                # Add more mappings as needed
            }


            entity_id_variable = device_name_to_entity_id.get(device_name_variable, "")

            if not entity_id_variable:
                print(f"Device with name '{device_name_variable}' not found in the mapping.")
                exit()

            connection = psycopg2.connect(
                database="thingsboard",
                user="thingsboard",
                password="postgres",
                host="192.168.1.85",
                port=5432,
            )
            cursor2 = connection.cursor(cursor_factory=DictCursor)
            

            query2 = f"""
            SELECT 
            entity_id, 
            ts, 
            uuid, 
            COALESCE(bool_v::TEXT, str_v, long_v::TEXT, dbl_v::TEXT, json_v::TEXT) AS actual_value
            FROM 
            ts_kv
            WHERE
            entity_id = '{entity_id_variable}'
            AND key = {key_id_result}
            ORDER BY 
            ts DESC
            LIMIT 1
            """

            cursor2.execute(query2)
            rows2 = cursor2.fetchall()

            if rows2:
                last_value = rows2[0]["actual_value"]
                dispatcher.utter_message(text=f"The latest value for {device_name_variable} is {last_value}.")
            else:
                dispatcher.utter_message(text=f"No data found for the specified device and sensor.")

        # Close the cursor and the database connection
            cursor2.close()
            connection.close()

            return []
    

# class action_asked_q1(Action):
#     def name(self) -> Text:
#         return "action_asked_q1"
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#             dispatcher.utter_message(text="could'nt get current temperature. please try again")
#             return []

# class action_asked_q2(Action):
#     def name(self) -> Text:
#         return "action_asked_q2"
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#             dispatcher.utter_message(text="could'nt get current temperature. please try again")
#             return []
    
# class action_asked_q3(Action):
#     def name(self) -> Text:
#         return "action_asked_q3"
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#             dispatcher.utter_message(text="could'nt get current temperature. please try again")
#             return []
    
# class action_asked_q4(Action):
#     def name(self) -> Text:
#         return "action_asked_q4"
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#             dispatcher.utter_message(text="could'nt get current temperature. please try again")
#             return []
    
# class action_asked_q5(Action):
#     def name(self) -> Text:
#         return "action_asked_q5"
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#             dispatcher.utter_message(text="could'nt get current temperature. please try again")
#             return []
    
# class action_asked_q6(Action):
#     def name(self) -> Text:
#         return "action_asked_q6"
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#             dispatcher.utter_message(text="could'nt get current temperature. please try again")
#             return []
    
# class action_asked_q7(Action):
#     def name(self) -> Text:
#         return "action_asked_q7"
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#             dispatcher.utter_message(text="could'nt get current temperature. please try again")
#             return []
    
# class action_asked_q8(Action):
#     def name(self) -> Text:
#         return "action_asked_q8"
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#             dispatcher.utter_message(text="could'nt get current temperature. please try again")
#             return []
    
# class action_asked_q9(Action):
#     def name(self) -> Text:
#         return "action_asked_q9"
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
#             dispatcher.utter_message(text="could'nt get current temperature. please try again")
#             return []
    
# class action_asked_q10(Action):
#     def name(self) -> Text:
#         return "action_asked_q10"
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
#             dispatcher.utter_message(text="could'nt get current temperature. please try again")
#             return []

