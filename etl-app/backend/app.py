from flask import Flask, request, jsonify
# from flask_cors import cross_origin
from flask_cors import CORS
import pandas as pd
import numpy as np
from sqlalchemy import create_engine

app = Flask(__name__)
CORS(app,  resources={
     r"/*": {"Access-Control-Allow-Origin": "http://localhost:3001"}})


@app.route('/')
def home():
    return "ETL API is running!"


@app.after_request
def add_x_content_type_options(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    # Cache for 1 hour
    response.headers['Cache-Control'] = 'private, max-age=3600'
    return response


@app.route('/etl', methods=['OPTIONS', 'POST'])
# @cross_origin()  # Allow cross-origin requests
def etl():

    if request.method == 'OPTIONS':
        # Handle CORS preflight request
        response = jsonify({"message": "Preflight request allowed"})
        response.status_code = 200
        return response

    if request.method == 'POST':
        print("Request received: {format(request.json)}")
        data = request.json
        source_data = extract_data(data['source'])
        transformed_data = transform_data(source_data)
        dbname = "postgresql"
        load_data(transformed_data, data['destination'], dbname)
        return jsonify({"message": "ETL process completed successfully!"}), 200


def extract_data(source):
    if source == 'api':
        # data extraction from API
        import requests
        response = requests.get('https://api.example.com/data')
        return pd.json_normalize(response.json())
    elif source == 'csv':
        # data extraction from CSV
        return pd.read_csv('data.csv')
    else:
        raise ValueError("Unsupported data source")


def transform_data(data):
    # Example transformation - apply AI /ML models transformations
    data['transformed_column'] = data['original_column']*np.random.random()
    return data


def load_data(data, destination, dbname):
    if destination == 'database' and dbname == "sqlite":
        # Load data into a database
        engine = create_engine('sqlite:///example.db')
        data.to_sql('table_name', con=engine, if_exists='replace', index=False)
    elif destination == 'database' and dbname == "postgresql":
        # Load data into PostgreSQL
        engine = create_engine(
            'postgresql://username:password@localhost:5432/{destination}')
        data.to_sql('transformed_table', con=engine,
                    if_exists='replace', index=False)

    elif destination == 'csv':
        # Save to CSV
        data.to_csv('transformed_data.csv', index=False)
    else:
        raise ValueError("Unsupported data destination")


if __name__ == '__main__':
    app.run(debug=True)
