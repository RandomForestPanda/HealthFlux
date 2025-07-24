
from flask import Flask, jsonify
import json
import os

app = Flask(__name__)

def read_json_from_directory(directory):
    part_files = [f for f in os.listdir(directory) if f.startswith('part-')]
    if not part_files:
        raise FileNotFoundError(f"No part files found in {directory}")
    file_path = os.path.join(directory, part_files[0])
    with open(file_path, 'r') as f:
        # Read all lines and parse as a list of JSON objects
        lines = [json.loads(line.strip()) for line in f if line.strip()]
        return lines

@app.route('/api/spark/top-diagnoses', methods=['GET'])
def get_top_diagnoses():
    try:
        if not os.path.exists('top_diagnoses.json'):
            print("Error: top_diagnoses.json directory not found")
            return jsonify({'error': 'top_diagnoses.json directory not found'}), 500
        data = read_json_from_directory('top_diagnoses.json')
        print("Serving top_diagnoses.json")
        return jsonify(data)
    except Exception as e:
        print(f"Error in top-diagnoses endpoint: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/spark/readmissions', methods=['GET'])
def get_readmissions():
    try:
        if not os.path.exists('readmissions.json'):
            print("Error: readmissions.json directory not found")
            return jsonify({'error': 'readmissions.json directory not found'}), 500
        data = read_json_from_directory('readmissions.json')
        print("Serving readmissions.json")
        return jsonify(data)
    except Exception as e:
        print(f"Error in readmissions endpoint: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("Starting Flask server on port 5000")
    app.run(port=5000, debug=True)
