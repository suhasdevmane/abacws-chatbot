# app.py

from flask import Flask, request, jsonify, render_template_string
from transformers import BartTokenizer, BartForConditionalGeneration, T5Tokenizer, T5ForConditionalGeneration
from SPARQLWrapper import SPARQLWrapper, JSON
import torch
import logging
# Constants for API endpoints
TRANSLATE_URL = "http://t5-t5:5000/translate"
SUMMARIZE_URL = "http://t5-t5:5000/summarize"
SPARQL_ENDPOINT = "http://jena-fuseki:3030/abacws-sensor-network/sparql"
# Set up logging
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)

# Load the model and tokenizer for BART
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model_path1 = "./T5-NL2SPARQL/trained"
tokenizer1 = T5Tokenizer.from_pretrained(model_path1)
model1 = T5ForConditionalGeneration.from_pretrained(model_path1).to(device)
# model_path1 = "./BART-NL2SPARQL/trained"                  # USE THIS MODEL ALTERNATEVELY
# tokenizer1 = BartTokenizer.from_pretrained(model_path1)
# model1 = BartForConditionalGeneration.from_pretrained(model_path1).to(device)

# Load the model and tokenizer for T5
model_path2 = "./T5-SPARQL2QA/trained"
tokenizer2 = T5Tokenizer.from_pretrained(model_path2)
model2 = T5ForConditionalGeneration.from_pretrained(model_path2).to(device)

# HTML template for the combined home page
html_template = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SPARQL Translator</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f0f0f5;
            margin: 0;
            padding: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
        }
        h1 {
            color: #333;
            text-align: center;
            width: 10%;
        }
        h2 {
            color: #555;
        }
        .container {
            display: flex;
            flex-wrap: wrap;
            width: 90%;
            max-width: 1200px;
            padding: 20px;
            justify-content: space-between;
        }
        .form-container {
            background: #fff;
            padding: 20px;
            margin: 10px;
            border-radius: 10px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            flex: 1;
            max-width: 45%;
            box-sizing: border-box;
        }
        .full-width {
            max-width: 100%;
        }
        label {
            display: block;
            margin-bottom: 10px;
            color: #333;
        }
        input[type="text"], textarea {
            width: calc(100% - 20px);
            padding: 10px;
            margin-bottom: 20px;
            border: 1px solid #ccc;
            border-radius: 5px;
            box-sizing: border-box;
        }
        input[type="submit"] {
            background: #007BFF;
            color: #fff;
            padding: 10px 20px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
        }
        input[type="submit"]:hover {
            background: #0056b3;
        }
        textarea {
            width: calc(100% - 20px);
            padding: 10px;
            border: 1px solid #ccc;
            border-radius: 5px;
            box-sizing: border-box;
        }
        @media (max-width: 900px) {
            .form-container {
                max-width: 100%;
            }
            .container {
                flex-direction: column;
                align-items: center;
            }
        }
    </style>
</head>
<body>
    <h1>Welcome to the SPARQL Translator and Explainer</h1>
    <div class="container">
        <div class="form-container">
            <h2>Translate Natural Language to SPARQL</h2>
            <form action="/translate" method="post">
                <label for="query">Enter your natural language query:</label><br><br>
                <input type="text" id="query" name="query" value="{{ query or '' }}" style="width: 100%;"><br><br>
                <input type="submit" value="Translate">
            </form>
            {% if sparql_query %}
                <h2>SPARQL Query:</h2>
                <textarea id="sparql_query" name="sparql_query" rows="4" cols="50" readonly>{{ sparql_query }}</textarea>
            {% endif %}
        </div>

        <div class="form-container">
            <h2>Formatted SPARQL Query</h2>
            <form action="/execute_sparql" method="post">
                <label for="sparql_query">Enter Generated SPARQL query from the first box:</label><br><br>
                <textarea id="sparql_query" name="sparql_query" rows="10" cols="50">{{ sparql_query or '' }}</textarea><br><br>
                <input type="submit" value="Execute">
            </form>
            {% if formatted_results %}
                <h2>Results:</h2>
                <textarea id="formatted_results" name="formatted_results" rows="10" cols="50" readonly>{{ formatted_results }}</textarea>
            {% endif %}
        </div>

        <div class="form-container full-width">
            <h2>Explain SPARQL Output</h2>
            <form action="/summarize" method="post">
                <label for="en">Enter your natural language query used in first box:</label><br><br>
                <input type="text" id="en" name="en" value="{{ en or '' }}" style="width: 100%;"><br><br>
                <label for="response">Enter your formatted SPARQL query generated in the second box:</label><br><br>
                <input type="text" id="response" name="response" value="{{ response or '' }}" style="width: 100%;"><br><br>
                <input type="submit" value="Translate">
            </form>
            {% if explanation %}
                <h2>Explanation:</h2>
                <textarea id="explanation" name="explanation" rows="10" cols="80" readonly>{{ explanation }}</textarea>
            {% endif %}
        </div>
    </div>
</body>
</html>
'''

@app.route('/')
def home():
    return render_template_string(html_template)

@app.route('/translate', methods=['POST'])
def translate():
    try:
        if request.content_type == 'application/json':
            data = request.json
            query = data.get('query')
        else:
            query = request.form.get('query')
        
        if not query:
            if request.content_type == 'application/json':
                return jsonify({"error": "No query provided"}), 400
            else:
                return render_template_string(html_template, sparql_query="No query provided")

        inputs = tokenizer1(query, return_tensors="pt").to(device)
        outputs = model1.generate(
            **inputs,
            max_length=300,
            num_beams=4,
            no_repeat_ngram_size=10,
            early_stopping=True
        )
        generated_text1 = tokenizer1.decode(outputs[0], skip_special_tokens=True)

        if request.content_type == 'application/json':
            return jsonify({"sparql_query": generated_text1})
        else:
            return render_template_string(html_template, sparql_query=generated_text1)
    except Exception as e:
        logging.error(f"Error in translate: {e}")
        return jsonify({"error": str(e)}), 500
    
@app.route('/summarize', methods=['POST'])
def summarize():
    try:
        # Initialize variable for the input data
        input_data = None

        # Check the content type to determine how to process the input
        if request.content_type == 'application/json':
            data = request.json
            en = data.get('en')
            response = data.get('response')
            if not en or not response:
                return jsonify({"error": "No input question and formatted query provided"}), 400
            input_data = en + " " + response
        elif request.content_type == 'text/plain':
            # Handle plain text input as a single string
            input_data = request.data.decode('utf-8')
        else:
            en = request.form.get('en')
            response = request.form.get('response')
            if not en or not response:
                return render_template_string(html_template, explanation="Invalid input. Please provide both the natural language query and the SPARQL response.")
            input_data = en + " " + response

        # Validate input_data
        if not input_data:
            return jsonify({"error": "No valid input provided"}), 400

        inputs = tokenizer2(input_data, return_tensors="pt", max_length=1024, truncation=True).to(device)

        outputs = model2.generate(
            **inputs,
            max_length=350,
            num_beams=4,
            no_repeat_ngram_size=10,
            early_stopping=True
        )

        generated_text2 = tokenizer2.decode(outputs[0], skip_special_tokens=True)

        # Return the summary based on the request type
        if request.content_type == 'application/json':
            return jsonify({'explanation': generated_text2})
        elif request.content_type == 'text/plain':
            return generated_text2  # Return plain text
        else:
            return render_template_string(html_template, explanation=generated_text2)

    except Exception as e:
        logging.error(f"Error in summarize: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/execute_sparql', methods=['POST'])
def execute_sparql():
    try:
        sparql_query = request.form.get('sparql_query')

        final_sparql_query_template = """
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX bldg: <http://abacwsbuilding.cardiff.ac.uk/abacws#>
        PREFIX brick: <https://brickschema.org/schema/Brick#>
        PREFIX owl: <http://www.w3.org/2002/07/owl#>
        PREFIX sh: <http://www.w3.org/ns/shacl#>
        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
        """

        if sparql_query:
            final_sparql_query = final_sparql_query_template + sparql_query
        else:
            return jsonify({"error": "No SPARQL query to execute"}), 400

        # Use container name instead of localhost
        endpoint_url = "http://jena-fuseki:3030/abacws-sensor-network/sparql"

        logging.debug(f"Final SPARQL Query: {final_sparql_query}")
        logging.debug(f"Endpoint URL: {endpoint_url}")

        def execute_sparql_query(sparql_query, endpoint_url):
            sparql = SPARQLWrapper(endpoint_url)
            sparql.setQuery(sparql_query)
            sparql.setReturnFormat(JSON)
            results = sparql.query().convert()
            return results

        try:
            results = execute_sparql_query(final_sparql_query, endpoint_url)
        except Exception as e:
            logging.error(f"Error executing SPARQL query: {e}")
            return jsonify({"error": str(e)}), 500

        prefix_mappings = {
            "http://abacwsbuilding.cardiff.ac.uk/abacws#": "bldg:",
            "https://brickschema.org/schema/Brick#": "brick:",
            "http://www.w3.org/1999/02/22-rdf-syntax-ns#": "rdf:",
            "http://www.w3.org/2000/01/rdf-schema#": "rdfs:",
            "http://www.w3.org/2002/07/owl#":"owl:",
            "http://www.w3.org/ns/shacl#":"sh:",
            "http://www.w3.org/2001/XMLSchema#":"xsd:"
        }

        def remove_prefix(uri, prefix_mappings):
            for prefix, replacement in prefix_mappings.items():
                if uri.startswith(prefix):
                    return uri.replace(prefix, replacement)
            return uri

        def format_results(results_bindings, prefix_mappings):
            response_lines = []
            for binding in results_bindings:
                formatted_binding = {var: remove_prefix(binding[var]['value'], prefix_mappings) for var in binding}
                response_lines.append(", ".join(f"{var}: {formatted_binding[var]}" for var in formatted_binding))
            return "\n".join(response_lines)

        results_bindings = results.get("results", {}).get("bindings", [])
        if results_bindings:
            formatted_results = format_results(results_bindings, prefix_mappings)
        else:
            formatted_results = "No results found."

        logging.debug(f"Formatted Results: {formatted_results}")

        return render_template_string(html_template, formatted_results=formatted_results, sparql_query=sparql_query)
    except Exception as e:
        logging.error(f"Error in execute_sparql: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
