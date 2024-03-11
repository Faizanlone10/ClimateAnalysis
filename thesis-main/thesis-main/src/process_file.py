import pandas as pd
import streamlit as st
from stations  import station_details
import numpy as np

def process_txt_file(uploaded_file):
    if uploaded_file:
        if uploaded_file.type == "text/plain":
            text = uploaded_file.read().decode('utf-8')
            data = [line.split(';') for line in text.split('\n')]
            header = data[0]
            data = data[1:]

            # Convert to DataFrame
            df = pd.DataFrame(data, columns=header)

            # Data processing
            numeric_columns = ['STATIONS_ID', 'MESS_DATUM']
            df[numeric_columns] = df[numeric_columns].apply(pd.to_numeric, errors='coerce')
            df['MESS_DATUM'] = pd.to_datetime(df['MESS_DATUM'], format='%Y%m%d').dt.strftime('%d/%m/%Y')
            station_id = df['STATIONS_ID'].iloc[0]
            st.success('File loaded successfully')
            st.markdown('---')
            st.warning("Analysis file with Station ID: " + str(station_id))

            station_details(station_id)

            # Replace -999 with 'NA' in specific columns
            columns_to_replace_na = ['STATIONS_ID','  FX', '  FM', ' SDK', '  NM', '  PM', ' TMK', ' TXK', ' TNK', ' TGK', ' VPM', ' UPM']
            df[columns_to_replace_na] = df[columns_to_replace_na].replace('-999', np.nan)
            df[columns_to_replace_na] = df[columns_to_replace_na].replace(-999, np.nan)
            df[columns_to_replace_na] = df[columns_to_replace_na].replace('  -999', np.nan)
            df[columns_to_replace_na] = df[columns_to_replace_na].replace('   -999', np.nan)
            df[columns_to_replace_na] = df[columns_to_replace_na].replace(' -999', np.nan)
            df[columns_to_replace_na] = df[columns_to_replace_na].replace('    -999', np.nan)

            # Create the 'Specific Humidity' (SH) column
            df[' VPM'] = pd.to_numeric(df[' VPM'], errors='coerce')  # Convert 'VPM' to numeric, handling missing values
            df['SH'] = (((0.622 * df[' VPM']) / (1005 - (0.378 * df[' VPM'])))*1000)
            # Update selected_columns to match your actual columns
            selected_columns = ['STATIONS_ID','MESS_DATUM', '  FX', '  FM', ' SDK', '  NM', '  PM', ' TMK', ' TXK', ' TNK', ' TGK', ' VPM', ' UPM','SH']

            # Check if the desired columns exist in the DataFrame
            missing_columns = [col for col in selected_columns if col not in df.columns]
            st.markdown('---')

            if missing_columns:
                return f"Error: Missing columns in the uploaded file: {missing_columns}"
            return df[selected_columns]
        else:
            return None
    else:
        return None
    
# Create a mapping of column name replacements
column_mapping = {
    'MESS_DATUM': 'Reference Date',
    '  FX': 'Maximum Wind Gust (m/s)',
    '  FM': 'Mean Wind Velocity (m/s)',
    ' SDK': 'Sunshine Duration (h)',
    '  NM': 'Mean Cloud Cover (1/8)',
    '  PM': 'Mean Pressure (hPa)',
    ' TMK': 'Mean Temperature (°C)',
    ' TXK': 'Maximum Temperature (2m height) (°C)',
    ' TNK': 'Minimum Temperature (2m height) (°C)',
    ' TGK': 'Minimum Air Temperature (5cm above ground) (°C)',
    ' VPM' : 'daily mean of vapor pressure (hPa)',
    ' UPM':'daily mean of relative humidity (%)',
    'SH':'Specific Humidity (g/kg)'
}

def rename_columns(df):
    # Rename the columns based on the mapping
    df = df.rename(columns=column_mapping)
    return df


def process_output_file(uploaded_file):
    if uploaded_file is not None:
        data = pd.read_csv(uploaded_file, encoding='latin1')
        data['Receptor'] = 'R10'
        data = data[(data['u (m/s)'] != '(in terrain)')]
        return data
    
def filter_output_file(data, selected_z_value):
    filtered_data = data[data['z (m)'] == selected_z_value]
    return filtered_data


def process_specific_data_file(file):
    if file is not None:
        df = pd.read_csv(file)
        return df
    
def filter_specific_data_file(df):
    df = df[df['Data'] != -999]
    df['Data'] = df['Data'].abs()
    return df