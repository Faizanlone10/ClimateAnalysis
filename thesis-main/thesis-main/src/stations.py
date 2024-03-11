import streamlit as st
import os

def format_station_id(station_id):
    # Convert the station_id to an integer, trim the .0, and format it to have 5 digits with leading zeros
    formatted_id = f"{int(station_id):05d}"
    return formatted_id

def parse_station_details(station_details_text):
    # Split the lines and parse them into a dictionary
    lines = station_details_text.split('\n')
    station_data = {}
    
    for line in lines:
        parts = line.split(None, 1)
        if len(parts) == 2:
            key, value = parts
            station_data[key] = value.strip()

    return station_data

def extract_alphabetic(value):
    # Extract alphabetic characters and spaces
    alphabetic_value = ''.join(char if char.isalpha() or char.isspace() else '' for char in value)
    return alphabetic_value

def station_details(station_id):
    formatted_id = format_station_id(station_id)
    # Get the absolute path of the directory containing the script
    script_directory = os.path.dirname(os.path.realpath(__file__))

    # Construct the absolute path to the file
    station_details_file = os.path.join(script_directory, "resources/stations.txt")

    # Read the entire station details file into a string
    with open(station_details_file, 'r') as file:
        station_details_text = file.read()

    # Parse the station details into a dictionary
    station_data = parse_station_details(station_details_text)

    station_details_dict = {}
    for key, value in station_data.items():
        if key == formatted_id:
            station_details_dict[key] = value

    alphanumeric_value = extract_alphabetic(str(station_details_dict))
    # Display station details as a table with column names
    st.header('Station Name: ' + alphanumeric_value)

# Example usage in a Streamlit app
station_id = st.text_input("Enter Station ID:", "12345.0")
if st.button("Get Station Details"):
    station_details(station_id)
