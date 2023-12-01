import requests
import time
import random
import json


access_tokens = [
    "bJtR9Q72YuFnrlauOz2I",
    "cjS6zpU57XwclQf31YsH",
    "hQDoHevlPTBiHukOy3rA",
    "1nCMHLF10N5XDUSvGVCU",
    "ZfaupINUEUhJ1Dn3lHGO",
    "cDIN9QzNN8CptommVRlO",
    "rhJAkl9S6pRBtkcfFrDY",
    "Z3UD5kYGKfeUlvGaE2fg",
    "KYGpekIKV6ZgnekuOsny",
    "z1oKFx9S57LCHO8tIv8T",
    "9hUTH56Tvuif0jMikGM9",
    "4MT7VWsyUv7cDuQcvYNY",
    "MEPYIKmcxs6QiHdChIlh",
    "J1Fn0WXVkiYyRXYya666",
    "GxIj5G0nBCg252rKLBYB",
    "ZDMNcntJcSDyiHdHXsvh",
    "kV4s5cd6usMAzBhas0DY",
    "9mnbPWAw0zPycZ5lsgpq",
    "WRv5yDaODnH2fXiO3FH6",
    "4W3KoKTyv54AP0HNgGMP",
    "7O7oywIPLR71YkaKhhDD",
    "WhXnfSuhoePcvLSTbzu0",
    "pKIgLkN8DzDnOI9KjQm3",
    "TYvszs2xGXFmz1944P1n",
    "N8TvJqj49HFZhVZnHL2o",
    "pEmsSNtKKiJx2Iry36V5",
    "3HN3tNJm3qXrAbF9YoAq",
    "OIl0HwBh6D4JgshHf4wB",
    "u9zgemN2v2f9FC5dhufz",
    "3NwrcyZR0wzAWrCMWnNl",
    "wB4LKJotiCQbhvItdOmh",
    "cVr9WVIejp4mIE1FiRFQ",
    "phXrZxYnm5gEAPEvLPca",
    "rXp0cpTzQVPMivSsIEmY",
]

api_endpoint = "http://localhost:8080/api/v1"


def generate_random_data():
    data = {
        "UV_light": round(random.uniform(0, 0.1), 2),
        "memsvalue": random.randint(300, 400),
        "PM1.0Atmospheric": random.randint(8, 10),
        "PM2.5Atmospheric": random.randint(12, 14),
        "PM10Atmospheric": random.randint(12, 14),
        "tVOC_Concentration": random.randint(18, 20),
        "CO2eq_Concentration": random.randint(390, 410),
        "MQ2_sensor_voltage": round(random.uniform(0.25, 0.35), 2),
        "MQ2_Rs_ratio": round(random.uniform(15, 16), 2),
        "rsroratio2": round(random.uniform(150, 160), 2),
        "MQ3_sensor_voltage": round(random.uniform(0.30, 0.35), 2),
        "MQ3_Rs_ratio": round(random.uniform(14, 16), 2),
        "rsroratio3": round(random.uniform(750, 770), 2),
        "hchoppmvalue": round(random.uniform(0, 0.01), 2),
        "HCHO_RS": round(random.uniform(95, 105), 2),
        "Air_Quality_lev": "Fresh air",
        "airQualityValue": random.randint(750, 800),
        "Light_value": random.randint(170, 175),
        "Visible_light": random.randint(260, 265),
        "IR_light": random.randint(270, 280),
        "MQ5_sensor_voltage": round(random.uniform(0.65, 0.75), 2),
        "MQ5_Rs_ratio": round(random.uniform(5.8, 6.2), 2),
        "rsroratio5": round(random.uniform(40, 42), 2),
        "MQ9_sensor_voltage": round(random.uniform(0.35, 0.40), 2),
        "MQ9_Rs_ratio": round(random.uniform(12, 13), 2),
        "rsroratio9": round(random.uniform(82, 84), 2),
        "NO2": random.randint(192, 196),
        "c2h5ch": random.randint(287, 291),
        "VOC": random.randint(245, 251),
        "co_gas": random.randint(176, 182),
        "co2value": random.randint(598, 608),
        "tempreture": round(random.uniform(30, 32), 2),
        "humidity": round(random.uniform(17, 19), 2),
        "lux": round(random.uniform(400, 700), 2),
        "o2per": round(random.uniform(19, 20), 2),
    }
    return data


while True:
    for access_token in access_tokens:
        data = generate_random_data()

        # Build the API URL for telemetry
        telemetry_url = f"{api_endpoint}/{access_token}/telemetry"

        # Set headers for the request
        headers = {
            "Content-Type": "application/json",
        }

        # Perform the HTTP POST request
        try:
            response = requests.post(telemetry_url, json=data, headers=headers)
            response.raise_for_status()  # Raise an HTTPError for bad responses
            # print(".")
        except requests.exceptions.RequestException as e:
            print(f"Error posting telemetry data: {e}")
            if "response" in locals():
                print(f"Response content: {response.text}")

    time.sleep(20)