ETL - Python ( Flask + React)


April 5, 2025
https://www.linkedin.com/feed/update/urn:li:activity:7312073864321146881





Building an AI-based ETL (Extract, Transform, Load) application involves multiple steps, including data extraction from sources, transforming that data, and loading it into a destination for analysis or storage. The front end can be built with React.js, while the backend and ETL processes can be managed using Python.

Git Source: https://github.com/jayamoorthi/ETL-Flask-React

I’ll walk you through the general approach and provide you with the source structure for the repository:
**
Project Overview**

Backend (Python): A Flask-based application to handle ETL tasks (Extract, Transform, Load).
Frontend (React): A React app to interact with the user, allowing them to initiate ETL operations.
Docker: We'll containerize both the backend and frontend to create a seamless, portable, and consistent environment.

**2. Project Structure**
   
Here’s how your directory structure might look like:

etl-app/
├── backend/
│   ├── app.py          # Flask API for ETL
│   ├── requirements.txt # Python dependencies
│   ├── Dockerfile          # Dockerfile for the backend
├── frontend/
|-------etl-webapp
│   |     ├── public/
│   |     ├── src/
│   |     │   ├── App.js      # Main React App
│   |     │   ├── ETLForm.js  # Form for ETL requests
│   |     │   └── index.js    # Entry point
│   |     ├── package.json    # React dependencies
│   |     ├── Dockerfile          # Dockerfile for the frontend
└── README.md           # Project info and setup instructions 



**1. Backend (Python - ETL Process)**

Dependencies:

Flask or FastAPI for setting up the API to handle requests.
pandas for data transformation.
sqlalchemy for database interaction.
numpy for any numerical transformations.
requests for API data extraction if needed.
aiomysql or psycopg2 for database connections, depending on your DB type.
sklearn, tensorflow, or pytorch for any AI-based transformations or predictions.



**ETL Process Overview:**

Extract: Pull data from different sources such as APIs, CSV files, databases, etc.
Transform: Perform data cleaning, processing, and possibly AI-based transformations.
Load: Store the transformed data into a database or file.



**Steps for Backend Setup:**

Create a API project for Backend through terminal using Vs code 

<code>mkdir etl-app

ETL-Flask-React> cd etl-app
ETL-Flask-React\etl-app> mkdir backend
ETL-Flask-React\etl-app> mkdir frontend 
Install Dependencies packages before create environment and activate

ETL-Flask-React\etl-app\backend> python -m venv myenv
ETL-Flask-React\etl-app\backend> myenv/scripts/activate
install packages 

ETL-Flask-React\etl-app\backend> pip install pandas scikit-learn flask flask-cors sqlalchemy numpy
</code>

Backend - Create Flask API for ETL

**Backend Setup (Python + Flask)**
**1. Backend - app.py:**

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
Backend - requirements.txt:

Flask
pandas
numpy
requests
sqlalchemy
psycopg2 
Backend - Dockerfile:

# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Define environment variable for Flask
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

# Run the application
CMD ["flask", "run"] 
run application using command > python app.py then browser open with  127.0.0.1:5000 port. 






then browser will see "ETL API is running!" 


2. Frontend Setup (React)
Create a react app using npx create-react-app command fromTerminal 

ETL-Flask-React\etl-app\frontend> npx create-react-app etl-webapp
1. Frontend - ETLForm.js:

import React, { useState } from 'react';
import axios from 'axios';
import { TextField, Button } from '@mui/material';

const ETLForm = () => {
  const [source, setSource] = useState('');
  const [destination, setDestination] = useState('');

  const handleSubmit = async (event) => {
    event.preventDefault();

    try {
      const response = await axios.post('http://backend:5000/etl', {
        source,
        destination
      });
      alert('ETL Process Completed!');
    } catch (error) {
      console.error('Error occurred while executing ETL:', error);
    }
  };

  return (
    <div>
      <h2>ETL Form</h2>
      <form onSubmit={handleSubmit}>
        <TextField
          label="Source"
          value={source}
          onChange={(e) => setSource(e.target.value)}
          required
        />
        <br />
        <TextField
          label="Destination"
          value={destination}
          onChange={(e) => setDestination(e.target.value)}
          required
        />
        <br />
        <Button type="submit" variant="contained">Run ETL</Button>
      </form>
    </div>
  );
};

export default ETLForm; 
 Frontend - App.js:

 import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import ETLForm from './ETLForm';

const App = () => {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<ETLForm />} />
      </Routes>
    </Router>
  );
};

export default App; 


Frontend - Dockerfile:

# Use the official Node.js image as a parent image
FROM node:16

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install dependencies
RUN npm install

# Make port 3000 available to the world outside this container
EXPOSE 3000

# Start the React app
CMD ["npm", "start"] 


3. Docker Compose Setup
To manage both the frontend and backend containers, we will use Docker Compose.

docker-compose.yml:

version: '3'
services:
  backend:
    build:
      context: ./backend
    container_name: backend
    ports:
      - "5000:5000"
    networks:
      - app-network
    depends_on:
      - db

  frontend:
    build:
      context: ./frontend
    container_name: frontend
    ports:
      - "3000:3000"
    networks:
      - app-network
    depends_on:
      - backend

  db:
    image: postgres:13
    container_name: postgres_db
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD: password
      POSTGRES_DB: etl_db
    ports:
      - "5432:5432"
    networks:
      - app-network

networks:
  app-network:
    driver: bridge 
Running the Application with Docker
Build and Start Containers: In the root directory of your project (where the docker-compose.yml file is located), run the following command to build and start the services:

docker-compose up --build
Accessing the Application:
Frontend: Visit http://localhost:3001 for the React application.
Backend: Flask API is running on http://localhost:5000.






Notes and Enhancements
AI Transformation: The transformation step in the backend can be enhanced using AI models from scikit-learn, TensorFlow, or PyTorch.
Authentication and Error Handling: Add proper authentication mechanisms and more error handling to ensure robustness.
Persist Data: Modify the database and table loading logic to match your actual destination.



 Conclusion: 
 Learning how to create project api with structure using python Flask Api as backend and frontend react app. Keep learning new and adatoping technology.thanks.

 happy weekend, see you bye bye! !. 
