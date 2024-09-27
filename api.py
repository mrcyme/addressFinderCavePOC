import geopandas as gpd
from flask import Flask, jsonify, request
from fuzzywuzzy import process
import pandas as pd
from flask_cors import CORS

# Load shapefiles
building_gdf = gpd.read_file('UrbAdm_SHP/geojson/UrbAdm_BUILDING.geojson')
address_point_gdf = gpd.read_file('UrbAdm_SHP/geojson/UrbAdm_ADDRESS_POINT.geojson')
street_surface_level0_gdf = gpd.read_file('UrbAdm_SHP/geojson/UrbAdm_STREET_SURFACE_LEVEL0.geojson')

# Initialize Flask app
app = Flask(__name__)
CORS(app)
# Function to find the closest street name
def find_closest_string(gdf, search_string, column_name='PN_NAME_FR'):
    if column_name not in gdf.columns:
        raise ValueError(f"Column '{column_name}' does not exist in the GeoDataFrame.")
    column_values = gdf[column_name].dropna().astype(str).tolist()
    closest_match, score = process.extractOne(search_string, column_values)
    return closest_match, {'score': score}

def get_bu_id(gdf, pn_name_fr, adrn):
    # Filter the GeoDataFrame based on PN_NAME_FR and ADRN
    pn_name_fr, _ = find_closest_string(address_point_gdf, pn_name_fr)
    filtered_gdf = gdf.loc[(gdf['PN_NAME_FR'] == pn_name_fr) & (gdf['ADRN'] == adrn)]
    
    # Check if any rows match the filter criteria
    if not filtered_gdf.empty:
        # Return the BU_ID of the first matching row
        return int(filtered_gdf.iloc[0]['BU_ID'])
    else:
        return None
    
# API endpoint to search for a street and return it as GeoJSON
@app.route('/search_street', methods=['GET'])
def search_street():
    street_name = request.args.get('street_name', '')
    if not street_name:
        return jsonify({"error": "Street name is required"}), 400

    closest, _ = find_closest_string(street_surface_level0_gdf, street_name)
    if closest:
        result_gdf = street_surface_level0_gdf[street_surface_level0_gdf['PN_NAME_FR'].str.contains(closest, na=False)]
        # Convert Timestamp objects to strings
        for col in result_gdf.columns:
            if pd.api.types.is_datetime64_any_dtype(result_gdf[col]):
                result_gdf[col] = result_gdf[col].astype(str)
        return result_gdf.to_json()
    else:
        return jsonify({"error": "Street not found"}), 404
    
@app.route('/search_building', methods=['GET'])
def search_building():
    street = request.args.get('street', '')
    number = request.args.get('number', '')
    if not street:
        return jsonify({"error": "Street name is required"}), 400
    if not number:
        return jsonify({"error": "Number is required"}), 400

    if street:
        bu_id = get_bu_id(address_point_gdf, street, number)
        if bu_id:
            result_gdf = building_gdf[building_gdf['ID'] == bu_id]
            for col in result_gdf.columns:
                if pd.api.types.is_datetime64_any_dtype(result_gdf[col]):
                    result_gdf[col] = result_gdf[col].astype(str)
        print(result_gdf)
        return result_gdf.to_json()
    else:
        return jsonify({"error": "Building not found"}), 404

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True, port=5000)
