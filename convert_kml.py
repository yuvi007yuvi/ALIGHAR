import fiona
import json
from shapely.geometry import shape
from shapely.geometry import mapping
import os

def convert_kml_to_geojson():
    # Get the directory of the script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Input KML file path
    kml_file = os.path.join(script_dir, 'Aligarh.kml')
    
    # Output GeoJSON file path
    geojson_file = os.path.join(script_dir, 'wards.geojson')
    
    try:
        # Read KML file
        with fiona.open(kml_file, driver='KML') as source:
            # Prepare GeoJSON structure
            features = []
            for i, feature in enumerate(source):
                geom = shape(feature['geometry'])
                properties = feature['properties']
                properties['id'] = f'ward_{i+1}'
                
                features.append({
                    'type': 'Feature',
                    'geometry': mapping(geom),
                    'properties': properties
                })
            
            # Create GeoJSON object
            geojson = {
                'type': 'FeatureCollection',
                'features': features
            }
        
        # Write to GeoJSON file
        with open(geojson_file, 'w') as f:
            json.dump(geojson, f)
            
        print(f'Successfully converted KML to GeoJSON: {geojson_file}')
        
    except Exception as e:
        print(f'Error converting file: {str(e)}')

if __name__ == '__main__':
    convert_kml_to_geojson()