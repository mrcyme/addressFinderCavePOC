# GeoJSON Display and Search Application

This project is a web application that displays multiple GeoJSON files on a map and allows users to search for streets and buildings. The application uses Flask for the backend and Leaflet.js for the frontend map display.

## Features

- Display multiple GeoJSON layers on a map.
- Search for streets by name and highlight them on the map.
- Search for buildings by street name and number and highlight them on the map.

## Requirements

- Python 3.x
- Flask
- Flask-Cors
- GeoPandas
- FuzzyWuzzy
- Python-Levenshtein
- Leaflet.js

## Installation

1. Clone the repository:

2. Install the required Python packages:
    ```bash
    pip install -r requirements.txt
    ```

3. Ensure you have the necessary GeoJSON files in the `UrbAdm_SHP/geojson/` directory:
    - `UrbAdm_BUILDING.geojson`
    - `UrbAdm_ADDRESS_POINT.geojson`
    - `UrbAdm_STREET_SURFACE_LEVEL0.geojson`

## Running the Application

1. Start the Flask API server:
    ```bash
    python api.py
    ```

2. Run the frontend with :
    ```bash
    python -m http.server
    ```

## API Endpoints

- `/search_street`: Search for a street by name.
    - Query parameter: `street_name` (required)
    - Example: `http://localhost:5000/search_street?street_name=Main%20Street`

- `/search_building`: Search for a building by street name and number.
    - Query parameters: `street` (required), `number` (required)
    - Example: `http://localhost:5000/search_building?street=Main%20Street&number=123`

## Usage

- Use the search controls at the bottom of the map to search for streets and buildings.
- The map will highlight the searched street or building in red or blue, respectively.

## License

This project is licensed under the MIT License.
