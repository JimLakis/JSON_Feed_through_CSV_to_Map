# Python v3.6
# April, 2019

import urllib.request
import json
import geoplotlib
from geoplotlib.utils import read_csv


def get_json(url):
    """ Opening an HTTP connection to the desired site, retreiving the JSON information and returning the JSON object. """
    def open_connection(url):
        """ Opening an HTTP connection to the desired site and returning an HTTP object. """
        http_response_obj = urllib.request.urlopen(url)
        return http_response_obj
    
    def acquire_json_decode(http_response_obj):
        """ Reading in the JSON, decoding it and returning a JSON object. """
        json_obj = http_response_obj.read().decode("utf-8")
        return json_obj
    
    print("Acquiring HTTP Response Object...\n")
    http_response_obj = open_connection(url)
    print("Acquiring the JSON feed...\n")
    json_obj = acquire_json_decode(http_response_obj)
    return json_obj


def json_loads_to_dictionary(json_obj):
    """ Reads through the JSON object replacing 'null' values with None AND converts the JSON obj to a dictionary. """
    entire_report_dictionary = json.loads(json_obj)
    print("JSON object converted to a dictionary\n")
    return entire_report_dictionary


def extract_records(entire_report_dictionary):
    """ Extracts and returns a 'flattened' list of records, each element of the list is a dictionary representing one record """
    def extract_number_of_records(entire_report_dictionary):
        """ Extracts the number of records (ie quakes reported) """
        if 'count' in entire_report_dictionary['metadata']:
            number_of_records = entire_report_dictionary['metadata']['count']
        #print(f"number_of_records: {number_of_records}")
        return number_of_records

    def extract_flatten_records(entire_report_dictionary, number_of_records):
        """ Flatten each record of nested dictionaries and lists into one dictionary (a record), per each element of a list """
        id_lon_lat = []
        for i in range(number_of_records):
            l = []
            l.append(entire_report_dictionary['features'][i]['id'])
            l.append(entire_report_dictionary['features'][i]['geometry']['coordinates'][0]) # Lon
            l.append(entire_report_dictionary['features'][i]['geometry']['coordinates'][1]) # Lat
            id_lon_lat.append(l)
        return id_lon_lat

    number_of_records = extract_number_of_records(entire_report_dictionary)
    id_lon_lat = extract_flatten_records(entire_report_dictionary, number_of_records)
    print("Flattened records obtained\n")
    return number_of_records, id_lon_lat


def main():
    """ Extracts latitude and longitude from the JSON feed, converts the list of dictionaries to a dataframe and then plot the coordinates via GeoPlotLib """
    url = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/1.0_month.geojson"
    json_obj = get_json(url)
    entire_report_dictionary = json_loads_to_dictionary(json_obj)
    number_of_records, id_lon_lat = extract_records(entire_report_dictionary)[0], extract_records(entire_report_dictionary)[1]
    
    print("writing to file\n")
    with open('id_coordinates.csv', 'wt') as textiowrapper:
        textiowrapper.writelines('name,lon,lat\n')
        for i in range(number_of_records):
            x = 0
            id_num = str(id_lon_lat[i][x])
            lon = str(id_lon_lat[i][x+1])
            lat = str(id_lon_lat[i][x+2])
            s = id_num + ',' + lon + ',' + lat
            textiowrapper.writelines(s + '\n')
            del x
    textiowrapper.close()
    print("done writing to file\n")

    print("mapping the data\n")
    data = read_csv('id_coordinates.csv')
    geoplotlib.dot(data)
    geoplotlib.show()
	
  
if __name__ == "__main__":
    main()