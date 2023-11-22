import tkinter as tk
from tkinter import ttk
from datetime import datetime
from SPARQLWrapper import SPARQLWrapper, JSON

# List of available devices and locations
available_devices = ["notwo", "airq", "c2h5ch", "cotwo", "co", "dust", "hcho", "hum", "light", "mqfive", "mqnine",
                     "mqthree", "mqtwo", "notwo", "oxy", "pir", "sound", "temp", "voc"]  # Add more devices as needed
available_locations = [f"5.{i:02}" for i in range(1, 35)]  # Add more locations as needed

def execute_sparql_query(sensor_name, sensor_location, start_datetime, end_datetime):
    sensor_subject = f"bldg:{sensor_name}{sensor_location}"

    sparql_query = f"""
    PREFIX bldg: <http://abacwsbuilding.cardiff.ac.uk/abacws#>
    PREFIX brick: <https://brickschema.org/schema/Brick#>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

    SELECT ?value ?timestamp
    WHERE {{
      {sensor_subject} rdf:type brick:Sensor ;
                     brick:hasValue ?value ;
                     brick:hasTimestamp ?timestamp .
      FILTER (?timestamp >= "{start_datetime}"^^xsd:dateTime && ?timestamp <= "{end_datetime}"^^xsd:dateTime)
    }}
    ORDER BY DESC(?timestamp)
    LIMIT 1
    """

    endpoint_url = "http://localhost:3030/abacws-sensor-network/sparql"

    sparql = SPARQLWrapper(endpoint_url)
    sparql.setQuery(sparql_query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    if "results" in results and "bindings" in results["results"] and results["results"]["bindings"]:
        latest_result = results["results"]["bindings"][0]
        value = latest_result["value"]["value"]
        timestamp = latest_result["timestamp"]["value"]
        result_label.config(text=f"Latest Sensor Value: {value}, Timestamp: {timestamp}")
    else:
        result_label.config(text="No results found.")




def on_submit():
    selected_device = device_combobox.get()
    selected_location = location_combobox.get()
    selected_start_date = start_date_combobox.get()
    selected_start_time = start_time_combobox.get()
    selected_end_date = end_date_combobox.get()
    selected_end_time = end_time_combobox.get()

    start_datetime = f"{selected_start_date}T{selected_start_time}"
    end_datetime = f"{selected_end_date}T{selected_end_time}"

    execute_sparql_query(selected_device, selected_location, start_datetime, end_datetime)

# Create the main window
root = tk.Tk()
root.title("Sensor Query GUI")

# Device selection
device_label = ttk.Label(root, text="Choose sensor name:")
device_combobox = ttk.Combobox(root, values=available_devices)
device_combobox.set(available_devices[0])

# Location selection
location_label = ttk.Label(root, text="Choose sensor location:")
location_combobox = ttk.Combobox(root, values=available_locations)
location_combobox.set(available_locations[0])

# Start date selection
start_date_label = ttk.Label(root, text="Choose start date:")
start_date_combobox = ttk.Combobox(root, values=[datetime.now().strftime("%Y-%m-%d")])
start_date_combobox.set(datetime.now().strftime("%Y-%m-%d"))

# Start time selection
start_time_label = ttk.Label(root, text="Choose start time:")
start_time_combobox = ttk.Combobox(root, values=[f"{i:02}:00" for i in range(24)])
start_time_combobox.set("00:00")

# End date selection
end_date_label = ttk.Label(root, text="Choose end date:")
end_date_combobox = ttk.Combobox(root, values=[datetime.now().strftime("%Y-%m-%d")])
end_date_combobox.set(datetime.now().strftime("%Y-%m-%d"))

# End time selection
end_time_label = ttk.Label(root, text="Choose end time:")
end_time_combobox = ttk.Combobox(root, values=[f"{i:02}:00" for i in range(24)])
end_time_combobox.set("23:59")

# Submit button
submit_button = ttk.Button(root, text="Submit", command=on_submit)

# Result label
result_label = ttk.Label(root, text="")

# Layout
device_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
device_combobox.grid(row=0, column=1, padx=10, pady=5)

location_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
location_combobox.grid(row=1, column=1, padx=10, pady=5)

start_date_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")
start_date_combobox.grid(row=2, column=1, padx=10, pady=5)

start_time_label.grid(row=3, column=0, padx=10, pady=5, sticky="w")
start_time_combobox.grid(row=3, column=1, padx=10, pady=5)

end_date_label.grid(row=4, column=0, padx=10, pady=5, sticky="w")
end_date_combobox.grid(row=4, column=1, padx=10, pady=5)

end_time_label.grid(row=5, column=0, padx=10, pady=5, sticky="w")
end_time_combobox.grid(row=5, column=1, padx=10, pady=5)

submit_button.grid(row=6, column=0, columnspan=2, pady=10)

result_label.grid(row=7, column=0, columnspan=2, pady=10)

# Start the Tkinter event loop
root.mainloop()
