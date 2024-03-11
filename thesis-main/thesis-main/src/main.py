import streamlit as st
import pandas as pd
from upload_file import file_upload
from process_file import process_txt_file
from process_file import rename_columns
from layout import set_page_layout 
import numpy as np
import matplotlib.pyplot as plt
from outputmain import output_main
from specificOutputAnalysis import specific_output_main

def main():
    set_page_layout()
    st.title('Welcome to Climate Data Analysis')
    st.markdown('---')

    # Create a sidebar menu with options
    menu_option = st.sidebar.selectbox("Select Option", ["Home", "Select Date Range for CDC Analysis", "File Comparison of CDC Files","Envi-met Receptor Analysis","Specific Output Data Analysis"])

    if menu_option == "Home":
        st.write("Welcome to the Climate Data Analysis Home Page!")
        st.markdown("Select an option from left window 👈")
        
        heartbeat_code = """
<!DOCTYPE html>
<html>
<head>
    <style>
        .heart {
            display: inline-block;
            animation: heartbeat 1s infinite;
            font-size: 30px;
        }

        @keyframes heartbeat {
            0% {
                transform: scale(1);
            }
            50% {
                transform: scale(1.3);
            }
            100% {
                transform: scale(1);
            }
        }
    </style>
</head>
<body>
    <h1>Made with <span class="heart">❤️</span> by Faizan Bashir Lone</h1>
</body>
</html>
"""

        st.markdown(heartbeat_code, unsafe_allow_html=True)

    elif menu_option == "Select Date Range for CDC Analysis":
        st.sidebar.subheader("Select Date Range for CDC Analysis")
        uploaded_file = file_upload()
        processed_data = process_txt_file(uploaded_file)
        if isinstance(processed_data, pd.DataFrame) and 'MESS_DATUM' in processed_data.columns:
            select_date_range(processed_data)
        else:
            st.warning("No valid data to select date range. Upload and process data first.")

    elif menu_option == "File Comparison of CDC Files":
        st.sidebar.subheader("File Comparison of CDC Files")
        uploaded_file1 = st.file_uploader("Upload File 1")
        processed_file1 = {}
        if uploaded_file1:
            processed_file1 = process_txt_file(uploaded_file1)
        else:
            st.warning("Upload both files for comparison.")
        uploaded_file2 = st.file_uploader("Upload File 2")
        processed_file2 = {}
        if uploaded_file2:
            processed_file2 = process_txt_file(uploaded_file2)
        else:
            st.warning("Upload both files for comparison.")

        if isinstance(processed_file1, pd.DataFrame) and isinstance(processed_file2, pd.DataFrame):
            if st.sidebar.checkbox("Full Comparison", True):
                if st.button("Perform Full Comparison Analysis"):
                    year_comparison_analysis(processed_file1, processed_file2)
        if st.sidebar.checkbox("Yearly Comparison"):
            if st.button("Perform Yearly Comparison Analysis Based on Temperature"):
                file_comparison(processed_file1, processed_file2)
    elif menu_option == "Envi-met Receptor Analysis":
        st.sidebar.subheader("Envi-met Receptor Analysis")
        output_main()
    elif menu_option == "Specific Output Data Analysis":
        st.sidebar.subheader("Specific Output Data Analysis")
        specific_output_main()
    else:
        st.warning("Error processing files. Make sure the files are valid.")


def year_comparison_analysis(processed_file1, processed_file2):
    temperature_comparison(processed_file1, processed_file2)
    humidity_comparison(processed_file1, processed_file2)
    wind_comparison(processed_file1, processed_file2)

def temperature_comparison(processed_file1, processed_file2):
    overall_comparison_analysis(processed_file1, processed_file2, ' TMK', 'Mean Temperature (°C)')

def humidity_comparison(processed_file1, processed_file2):
    overall_comparison_analysis(processed_file1, processed_file2, ' UPM', 'daily mean of relative humidity (%)')

def wind_comparison(processed_file1, processed_file2):
    overall_comparison_analysis(processed_file1, processed_file2, '  FM', 'Mean Wind Velocity (m/s)')

def overall_comparison_analysis(processed_file1, processed_file2, column_name, plot_title):
    file1_station_id = processed_file1['STATIONS_ID'].iloc[0]
    file2_station_id = processed_file2['STATIONS_ID'].iloc[0]

    if column_name == ' TMK':
        st.title("Mean Temperature Analysis")
    elif column_name == ' UPM':
        st.title("Daily mean of relative humidity Analysis")
    elif column_name == '  FM':
        st.title("Mean Wind Velocity Analysis")
    
    st.title(f'Running Comparison on Station id: {file1_station_id} and {file2_station_id}')

    # Assuming you have data_dict and other necessary variables defined

    # Get the data for the first file
    station_data_1 = processed_file1

    # Clean the specified column by replacing invalid values with NaN
    station_data_1[column_name] = pd.to_numeric(station_data_1[column_name], errors='coerce')
    # Remove NaN values to avoid issues with plotting
    cleaned_data_1 = station_data_1.dropna(subset=[column_name])
    if cleaned_data_1.empty:
        st.warning(f"Data for {file1_station_id} is empty after cleaning. Cannot generate plots.")
        return
    # Get the data for the second file
    station_data_2 = processed_file2

    # Clean the specified column by replacing invalid values with NaN
    station_data_2[column_name] = pd.to_numeric(station_data_2[column_name], errors='coerce')
    # Remove NaN values to avoid issues with plotting
    cleaned_data_2 = station_data_2.dropna(subset=[column_name])
    if cleaned_data_2.empty:
        st.warning(f"Data for {file2_station_id} is empty after cleaning. Cannot generate plots.")
        return
    
    cleaned_data_2['Date'] = pd.to_datetime(cleaned_data_2['MESS_DATUM'], format='%d/%m/%Y', errors='coerce')

    # Use the correct DataFrame for unique dates
    unique_dates1 = cleaned_data_2['Date'].dt.date.unique()

    min_date = min(unique_dates1)
    max_date = max(unique_dates1)
    st.success(f'Date Range of Analysis : Starts at {min_date} and Ends at {max_date}')

    # Create a boxplot for the full data
    plt.figure(figsize=(10, 6))
    plt.boxplot([cleaned_data_1[column_name], cleaned_data_2[column_name]],
                labels=[file1_station_id, file2_station_id],
                showfliers=False, patch_artist=True, boxprops=dict(facecolor='lightblue', color='blue'),
                medianprops=dict(color='black'))
    plt.title(f'Box Plot of {plot_title}')
    plt.xlabel("Station")
    plt.ylabel(plot_title)

    # Add a legend
    legend_labels = ['Data Distribution']
    legend_handles = [plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='lightblue', markersize=8)]

    plt.legend(legend_handles, legend_labels, loc='upper right', fontsize='xx-small')

    # Display the boxplot
    st.pyplot(plt)

    # Display a table with statistics (if needed)
    stat_table_data = {'Statistic': ['Mean', 'Min', 'Max', 'Q1', 'Q3'],
                        file1_station_id: [np.mean(cleaned_data_1[column_name]),
                                           np.min(cleaned_data_1[column_name]),
                                           np.max(cleaned_data_1[column_name]),
                                           np.percentile(cleaned_data_1[column_name], 25),
                                           np.percentile(cleaned_data_1[column_name], 75)],
                        file2_station_id: [np.mean(cleaned_data_2[column_name]),
                                           np.min(cleaned_data_2[column_name]),
                                           np.max(cleaned_data_2[column_name]),
                                           np.percentile(cleaned_data_2[column_name], 25),
                                           np.percentile(cleaned_data_2[column_name], 75)]}
    
    stat_df = pd.DataFrame(stat_table_data)
    # # Drop the index before displaying the table
    st.dataframe(stat_df)
    st.markdown('---')


def file_comparison(processed_file1, processed_file2):
    file1_station_id = processed_file1['STATIONS_ID'].iloc[0]
    file2_station_id = processed_file2['STATIONS_ID'].iloc[0]

    st.title(f'Running Comparison on Station id: {file1_station_id} and {file2_station_id}')

    # Assuming you have data_dict and other necessary variables defined

    # Get the data for the first file
    station_data_1 = processed_file1

    # Clean the 'TMK' column by replacing invalid values with NaN
    station_data_1[' TMK'] = pd.to_numeric(station_data_1[' TMK'], errors='coerce')
    # Remove NaN values to avoid issues with plotting
    cleaned_data_1 = station_data_1.dropna(subset=[' TMK'])
    # Calculate the yearly mean temperature for the first file
    cleaned_data_1['MESS_DATUM'] = pd.to_datetime(cleaned_data_1['MESS_DATUM'], errors='coerce')
    cleaned_data_1['Year'] = cleaned_data_1['MESS_DATUM'].dt.year
    yearly_mean_1 = cleaned_data_1.groupby('Year')[' TMK'].mean()

    # Get the data for the second file
    station_data_2 = processed_file2

    # Clean the 'TMK' column by replacing invalid values with NaN
    station_data_2[' TMK'] = pd.to_numeric(station_data_2[' TMK'], errors='coerce')
    # Remove NaN values to avoid issues with plotting
    cleaned_data_2 = station_data_2.dropna(subset=[' TMK'])
    # Calculate the yearly mean temperature for the second file
    cleaned_data_2['MESS_DATUM'] = pd.to_datetime(cleaned_data_2['MESS_DATUM'], errors='coerce')
    cleaned_data_2['Year'] = cleaned_data_2['MESS_DATUM'].dt.year   
    yearly_mean_2 = cleaned_data_2.groupby('Year')[' TMK'].mean()

    for year in sorted(set(yearly_mean_1.index) & set(yearly_mean_2.index)):
        # Data for the first file
        data_1 = cleaned_data_1[cleaned_data_1['Year'] == year][' TMK']

        # Data for the second file
        data_2 = cleaned_data_2[cleaned_data_2['Year'] == year][' TMK']

        # Combine data for both files
        all_data = [data_1, data_2]

        # Create a boxplot using Matplotlib
        plt.figure(figsize=(8, 6))
        plt.boxplot(all_data, labels=[file1_station_id, file2_station_id], showfliers=False, patch_artist=True,
                    boxprops=dict(facecolor='lightblue', color='blue'), medianprops=dict(color='black'))
        plt.title(f'Yearly Box Plot of Mean Temperature (°C) - {year}')
        plt.xlabel("Station")
        plt.ylabel("Temperature (TMK)")

        # Add a legend
        legend_labels = ['Mean Temperature', 'Min Temperature', 'Max Temperature', 'Q1', 'Q3']
        legend_handles = [plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='lightblue', markersize=8),
                          plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='lightblue', markersize=8),
                          plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='lightblue', markersize=8),
                          plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='lightblue', markersize=8),
                          plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='lightblue', markersize=8)]

        plt.legend(legend_handles, legend_labels, loc='upper right', fontsize='xx-small')

        # Display the boxplot
        st.pyplot(plt)

        # Display a table with statistics
        stat_table_data = {'Statistic': ['Mean', 'Min', 'Max', 'Q1', 'Q3'],
                           file1_station_id: [np.mean(data_1), np.min(data_1), np.max(data_1),
                                              np.percentile(data_1, 25), np.percentile(data_1, 75)],
                           file2_station_id: [np.mean(data_2), np.min(data_2), np.max(data_2),
                                              np.percentile(data_2, 25), np.percentile(data_2, 75)]}

        stat_df = pd.DataFrame(stat_table_data)
        # Drop the index before displaying the table
        st.dataframe(stat_df)
        st.markdown('---')



def select_date_range(data):
    date_formats = ['%d/%m/%Y', '%Y%m%d']  # Add more date formats as needed
    # Try multiple date formats for conversion
    for date_format in date_formats:
        data['MESS_DATUM'] = pd.to_datetime(data['MESS_DATUM'], format=date_format, errors='coerce')

        # Filter out rows with valid dates
        data = data.dropna(subset=['MESS_DATUM'])
        unique_dates = data['MESS_DATUM'].dt.date.unique()
        if unique_dates.size > 0:
            break  # Stop trying date formats once valid dates are found

    if unique_dates.size > 0:
        if st.sidebar.checkbox("General Analysis", True):
            perform_general_analysis(data, unique_dates)
        if st.sidebar.checkbox("Specific Analysis"):
            perform_specific_analysis(data, unique_dates)
        if st.sidebar.checkbox("Month Specific Analysis"):
            month_specific_analysis(data,unique_dates)
    else:
        st.warning("No valid dates found in the data.")


def month_specific_analysis(data,unique_dates):
    min_date = min(unique_dates)
    max_date = max(unique_dates) 
    st.subheader("Analyze Specific Parameters for Particular Months")

    selected_months = st.multiselect("Select Months", ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"])

    # Map selected month names to their corresponding numbers
    month_mapping = {
        "January": 1,
        "February": 2,
        "March": 3,
        "April": 4,
        "May": 5,
        "June": 6,
        "July": 7,
        "August": 8,
        "September": 9,
        "October": 10,
        "November": 11,
        "December": 12
    }

    selected_month_numbers = [month_mapping[month] for month in selected_months]

    # Step 2: Filter the data for selected months
    filtered_df = data[data['MESS_DATUM'].dt.month.isin(selected_month_numbers)]

    col1, col2 = st.columns(2)
    with col1:
        analyze_start_date = st.date_input("Enter Start date", min_date, min_value=min_date, max_value=max_date, key='analyze_start_date')
    with col2:
        analyze_end_date = st.date_input("Enter End date", max_date, min_value=min_date, max_value=max_date, key='analyze_end_date')


    col1, col2, col3= st.columns(3)
    if col1.button("Relative Humidity Analysis"):
        analyse_humidity(filtered_df, analyze_start_date, analyze_end_date)

    if col2.button("Temperature Analysis"):
        analyse_temperature(filtered_df, analyze_start_date, analyze_end_date)
    if col3.button("Mean Wind Velocity Analysis"):
        analyse_wind_velocity(filtered_df, analyze_start_date, analyze_end_date)



def perform_specific_analysis(data, unique_dates):
    min_date = min(unique_dates)
    max_date = max(unique_dates)  

    st.subheader("Analyze Specific Parameters")
    
    col1, col2 = st.columns(2)
    with col1:
        analyze_start_date = st.date_input("Enter Start date", min_date, min_value=min_date, max_value=max_date, key='analyze_start_date')
    with col2:
        analyze_end_date = st.date_input("Enter End date", max_date, min_value=min_date, max_value=max_date, key='analyze_end_date')

    col1, col2, col3 = st.columns(3)

    if col1.button("Relative Humidity Analysis"):
        analyse_humidity(data, analyze_start_date, analyze_end_date)

    if col2.button("Temperature Analysis"):
        analyse_temperature(data, analyze_start_date, analyze_end_date)
    if col3.button("Mean Wind Velocity Analysis"):
        analyse_wind_velocity(data, analyze_start_date, analyze_end_date)

def analyse_wind_velocity(data, analyze_start_date, analyze_end_date):
    mask = (data['MESS_DATUM'].dt.date >= analyze_start_date) & (data['MESS_DATUM'].dt.date <= analyze_end_date)
    filtered_df = data[mask]
    col1, col2 = st.columns(2)
    with col1:
        plot_wind_velocity_box_matplotlib(filtered_df)

    highest_wind_velocity_row = find_highest_wind_velocity(filtered_df)

    if highest_wind_velocity_row is not None:
        st.success("Row with Highest Mean Wind Velocity:")
        processed_highest_wind_velocity_row = rename_columns(pd.DataFrame(highest_wind_velocity_row).T)
        highest_wind_velocity_row_html = processed_highest_wind_velocity_row.to_html(index=False)
        st.markdown('<div class="scrolling-table">', unsafe_allow_html=True)
        st.markdown(highest_wind_velocity_row_html, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.warning("No data available for the selected date range.")

    lowest_wind_velocity_row = find_lowest_wind_velocity(filtered_df)

    if lowest_wind_velocity_row is not None:
        st.success("Row with Lowest Mean Wind Velocity:")
        processed_lowest_wind_velocity_row = rename_columns(pd.DataFrame(lowest_wind_velocity_row).T)
        lowest_wind_velocity_row_html = processed_lowest_wind_velocity_row.to_html(index=False)
        st.markdown('<div class="scrolling-table">', unsafe_allow_html=True)
        st.markdown(lowest_wind_velocity_row_html, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.warning("No data available for the selected date range.")

def plot_wind_velocity_box_matplotlib(data):
    if not data.empty:
        st.success("Box Plot for 'Mean Wind Velocity (m/s)' data within the selected date range:")
        
        # Clean the ' FM' column by replacing invalid values with NaN
        data['  FM'] = pd.to_numeric(data['  FM'], errors='coerce')

        # Remove NaN values to avoid issues with plotting
        cleaned_data = data.dropna(subset=['  FM'])
        
        if not cleaned_data.empty:
            # Create a boxplot using Matplotlib with color
            boxprops = dict(color='blue',facecolor='lightblue')
            plt.boxplot(cleaned_data['  FM'], showfliers=False, boxprops=boxprops, patch_artist=True)
            plt.title("Box Plot of Mean Wind Velocity (m/s)")
            plt.xlabel("Mean Wind Velocity (m/s)")
            plt.grid(True)
            # Display the plot
            st.pyplot(plt)

            # Display the statistics table
            stat_table_data = {
                'Statistic': ['Mean', 'Min', 'Max', 'Q1', 'Q3'],
                'Value': [cleaned_data['  FM'].mean(), cleaned_data['  FM'].min(), cleaned_data['  FM'].max(), cleaned_data['  FM'].quantile(0.25), cleaned_data['  FM'].quantile(0.75)],
            }

            stat_df = pd.DataFrame(stat_table_data)

            # Display the table without the index column
            st.dataframe(stat_df)
        else:
            st.warning("No valid data available for the selected date range.")
    else:
        st.warning("No data available for the selected date range.")

def find_highest_wind_velocity(data):
    # Remove rows where the 'FM' column contains only NaN values
    data_cleaned = data.dropna(subset=['  FM'], how='all')

    if not data_cleaned.empty:
        # Find the row with the highest wind velocity
        max_wind_velocity_row = data_cleaned.loc[data_cleaned['  FM'].idxmax()]
        return max_wind_velocity_row
    else:
        return None

def find_lowest_wind_velocity(data):
    data_cleaned = data.dropna(subset=['  FM'], how='all')

    if not data_cleaned.empty:
        # Find the row with the highest wind velocity
        min_wind_velocity_row = data_cleaned.loc[data_cleaned['  FM'].idxmin()]
        return min_wind_velocity_row
    else:
        return None

def analyse_temperature(data, analyze_start_date, analyze_end_date):
    mask = (data['MESS_DATUM'].dt.date >= analyze_start_date) & (data['MESS_DATUM'].dt.date <= analyze_end_date)
    filtered_df = data[mask]

    # Analyze TMK column
    analyse_temperature_column(filtered_df, ' TMK')
    st.markdown('---')
    st.markdown('---')

    # Analyze TXK column
    analyse_temperature_column(filtered_df, ' TXK')
    st.markdown('---')
    st.markdown('---')

    # Analyze TNK column
    analyse_temperature_column(filtered_df, ' TNK')
    st.markdown('---')
    st.markdown('---')

def analyse_temperature_column(filtered_df,column):
    if not filtered_df.empty:
        col1, col2 = st.columns(2)
        with col1:
            plot_temperature_box_matplotlib(filtered_df,column)
        with col2:
            highest_temp_row = find_highest_temperature(filtered_df,column)
            lowest_temp_row = find_lowest_temperature(filtered_df,column)

        if highest_temp_row is not None:
            st.success("Row with Highest Temperature:")
            processed_highest_temp_row = rename_columns(pd.DataFrame(highest_temp_row).T)
            highest_temp_row_html = processed_highest_temp_row.to_html(index=False)
            st.markdown('<div class="scrolling-table">', unsafe_allow_html=True)
            st.markdown(highest_temp_row_html, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.warning("No data available for the selected date range.")

        if lowest_temp_row is not None:
            st.success("Row with Lowest Temperature:")
            processed_lowest_temp_row = rename_columns(pd.DataFrame(lowest_temp_row).T)
            lowest_temp_row_html = processed_lowest_temp_row.to_html(index=False)
            st.markdown('<div class="scrolling-table">', unsafe_allow_html=True)
            st.markdown(lowest_temp_row_html, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.warning("No data available for the selected date range.")
    else:
        st.warning("No valid data available for the selected date range.")

def plot_temperature_box_matplotlib(data,column):
    if not data.empty:
        plt.figure(figsize=(8, 6))

        # Clean the 'TMK' column by replacing invalid values with NaN
        data[column] = pd.to_numeric(data[column], errors='coerce')

        # Remove NaN values to avoid issues with plotting
        cleaned_data = data.dropna(subset=[column])

        if not cleaned_data.empty:
            # Create a boxplot
            boxprops = dict(color='red',facecolor='maroon')
            plt.boxplot(cleaned_data[column], labels=['Temperature '], showfliers=False,boxprops =boxprops, patch_artist=True) 
            if column == ' TMK':
                plt.title("Box Plot of Mean Temperature (°C)")
            elif column == ' TXK':
                plt.title("Box Plot of Maximum Temperature (2m height) (°C)")
            elif column == ' TNK':
                plt.title("Box Plot of Minimum Temperature (2m height) (°C)")
            plt.xlabel("Measurement")
            plt.ylabel("Temperature (°C)")
            plt.grid(True)

            # Display the plot
            st.pyplot(plt)

            # Display table with mean, min, max, q1, q3
            stat_table_data = {
                'Statistic': ['Mean', 'Min', 'Max', 'Q1', 'Q3'],
                'Temperature ': [
                    cleaned_data[column].mean(),
                    cleaned_data[column].min(),
                    cleaned_data[column].max(),
                    cleaned_data[column].quantile(0.25),
                    cleaned_data[column].quantile(0.75),
                ]
            }
            stat_df = pd.DataFrame(stat_table_data)

            # Remove the index column
            stat_df = stat_df.set_index('Statistic')

            # Display the table
            st.dataframe(stat_df)
        else:
            st.warning("No valid data available for the selected date range.")
    else:
        st.warning("No data available for the selected date range.")       

def find_highest_temperature(data,column):
    max_temp_row = data.loc[data[column].idxmax()]
    return max_temp_row

def find_lowest_temperature(data,column):
    min_temp_row = data.loc[data[column].idxmin()]
    return min_temp_row

def analyse_humidity(data,analyze_start_date,analyze_end_date):
    mask = (data['MESS_DATUM'].dt.date >= analyze_start_date) & (data['MESS_DATUM'].dt.date <= analyze_end_date)
    filtered_df = data[mask]
    col1, col2 = st.columns(2)
    with col1:
        plot_humidity_box_matplotlib(filtered_df)

    highest_humidity_row = find_highest_humidity(filtered_df)

    if highest_humidity_row is not None:
        st.success("Row with Highest daily mean of relative humidity (%):")
        processed_highest_humidity_row = rename_columns(pd.DataFrame(highest_humidity_row).T)
        highest_humidity_row_html = processed_highest_humidity_row.to_html(index=False)
        st.markdown('<div class="scrolling-table">', unsafe_allow_html=True)
        st.markdown(highest_humidity_row_html, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.warning("No data available for the selected date range.")
    lowest_humidity_row = find_lowest_humidity(filtered_df)

    if lowest_humidity_row is not None:
        st.success("Row with Lowest Humidity:")
        processed_lowest_humidity_row = rename_columns(pd.DataFrame(lowest_humidity_row).T)
        lowest_humidity_row_html = processed_lowest_humidity_row.to_html(index=False)
        st.markdown('<div class="scrolling-table">', unsafe_allow_html=True)
        st.markdown(lowest_humidity_row_html, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.warning("No data available for the selected date range.")

def plot_humidity_box_matplotlib(data):
    if not data.empty:
        plt.figure(figsize=(8, 6))

        # Clean the ' UPM' column by replacing invalid values with NaN
        data[' UPM'] = pd.to_numeric(data[' UPM'], errors='coerce')

        # Remove NaN values to avoid issues with plotting
        cleaned_data = data.dropna(subset=[' UPM'])

        if not cleaned_data.empty:
            # Create a boxplot
            boxprops = dict(color='blue', facecolor='lightgreen')
            plt.boxplot(cleaned_data[' UPM'], showfliers=False, boxprops=boxprops,patch_artist=True)
            plt.title("Box Plot of daily mean of relative humidity (%)")
            plt.xlabel("daily mean of relative humidity (%)")
            plt.grid(True)

            # Display the plot
            st.pyplot(plt)

            # Display table with mean, min, max, q1, q3
            stat_table_data = {
                'Statistic': ['Mean', 'Min', 'Max', 'Q1', 'Q3'],
                'Humidity (UPM)': [
                    cleaned_data[' UPM'].mean(),
                    cleaned_data[' UPM'].min(),
                    cleaned_data[' UPM'].max(),
                    cleaned_data[' UPM'].quantile(0.25),
                    cleaned_data[' UPM'].quantile(0.75),
                ]
            }
            stat_df = pd.DataFrame(stat_table_data)

            # Remove the index column
            stat_df = stat_df.set_index('Statistic')

            # Display the table
            st.dataframe(stat_df)
        else:
            st.warning("No valid data available for the selected date range.")
    else:
        st.warning("No data available for the selected date range.")

def find_highest_humidity(data):
    max_humidity_row = data.loc[data[' UPM'].idxmax()]
    return max_humidity_row

def find_lowest_humidity(data):
    min_humidity_row = data.loc[data[' UPM'].idxmin()]
    return min_humidity_row  

def perform_general_analysis(data, unique_dates):
        matching_data = data.copy()
        min_date = min(unique_dates)
        max_date = max(unique_dates)
        st.subheader("Available Date Range: ")
        st.success(f"From {min_date} to {max_date}")
        st.markdown('---')

        st.subheader("Select a Date to check its Climate Data:")

        # Get the latest year from the data
        latest_year = max_date.year

        # Create separate dropdowns for year, month, and day side by side
        col1, col2, col3 = st.columns(3)
        with col1:
            selected_year = st.selectbox("Year", range(latest_year, min_date.year - 1, -1), index=0)
        with col2:
            selected_month = st.selectbox("Month", range(1, 13), index=0)
        with col3:
            selected_day = st.selectbox("Day", range(1, 32), index=0)

        if st.button("Perform Analysis"):
            display_selected_data(data, selected_year, selected_month, selected_day)

        st.markdown('---')
        st.subheader("Select a Date  Range to check its Climate Data and Display Date with Maximum temperature:")
        # Limit date input to the range of dates in the table
        col1, col2 = st.columns(2)
        with col1:
            start_date = st.date_input("Enter Start date", min_date, min_value=min_date, max_value=max_date)
        with col2:
            end_date = st.date_input("Enter End date", max_date, min_value=min_date, max_value=max_date)

        mask = (data['MESS_DATUM'].dt.date >= start_date) & (data['MESS_DATUM'].dt.date <= end_date)
        filtered_df = data[mask]

        col1, col2 , col3= st.columns(3)

        with col1:
            st.success("Click Below Button to do Analysis on: Analysis Based on Max Mean Temperature (°C),  highest daily mean of relative humidity (%)  and Lowest Mean Wind Velocity (m/s)")

        with col2:
            st.warning("Click Below Button to do Analysis on: Analysis Based on  Max Mean Temperature (°C), Highest Sunshine Duration (h) andLowest Mean Cloud Cover (1/8)")
        
        with col3:
            st.success("Click Below Button to do Analysis on: Analysis Based on  Mean Cloud Cover (1/8) Equal to 0 , Max Mean Temperature (°C), Highest Sunshine Duration (h) and Lowest Mean Wind Velocity (m/s) only in June July August month")

        

        if col1.button("Perform Analysis 1"):
            st.title("Analysis Based on Max Mean Temperature (°C),  highest daily mean of relative humidity (%)  and Lowest Mean Wind Velocity (m/s)")
            perform_analysis_1(filtered_df)

        if col2.button("Perform Analysis 2"):
            st.title("Analysis Based on  Max Mean Temperature (°C), Highest Sunshine Duration (h) andLowest Mean Cloud Cover (1/8)")
            perform_analysis_2(filtered_df) 
        if col3.button("Perform Analysis 3"):
            st.title("Analysis Based on  Mean Cloud Cover (1/8) Equal to 0 , Max Mean Temperature (°C), Highest Sunshine Duration (h) and Lowest Mean Wind Velocity (m/s)")
            perform_analysis_3(filtered_df)         
           
        st.markdown('---')

        perform_matching_analysis(data)
       
# Function to strip whitespace from all values in the DataFrame
def strip_whitespace(df):
    return df.applymap(lambda x: x.strip() if isinstance(x, str) else x)

def get_dependent_values(data, selected_column, prev_selected_values):
    df = data.copy()
    for col, val in prev_selected_values.items():
        df = df[df[col].str.strip() == val.strip()]
    return df[selected_column].astype(str).str.strip().unique()

def perform_matching_analysis(data):
    st.title('Search Data')

    # Extract unique values for each column
    unique_nm_values = get_dependent_values(data, '  NM', {})
    unique_sdk_values = get_dependent_values(data, ' SDK', {})
    unique_tmk_values = get_dependent_values(data, ' TMK', {})
    unique_fm_values = get_dependent_values(data, '  FM', {})

    # Dropdowns for user selection
    nm_value = st.selectbox('Select value for Mean Cloud Cover (1/8)', sorted(unique_nm_values))
    prev_selected = {'  NM': nm_value}

    sdk_values = get_dependent_values(data, ' SDK', prev_selected)
    sdk_value = st.selectbox('Select value for Sunshine Duration (h)', sorted(sdk_values))

    prev_selected[' SDK'] = sdk_value

    tmk_values = get_dependent_values(data, ' TMK', prev_selected)
    tmk_value = st.selectbox('Select value for Mean Temperature (°C)', sorted(tmk_values))

    prev_selected[' TMK'] = tmk_value

    fm_values = get_dependent_values(data, '  FM', prev_selected)
    fm_value = st.selectbox('Select value for Mean Wind Velocity (m/s)', sorted(fm_values))

    if st.button("Search"):
        matching_data = data.copy()  # Copy the original data for filtering
        
        # Remove whitespace from all values in the DataFrame
        matching_data = strip_whitespace(matching_data)

        filtered_result = matching_data[(matching_data['  FM'].str.strip() == fm_value.strip()) & 
                                        (matching_data[' SDK'].str.strip() == sdk_value.strip()) & 
                                        (matching_data['  NM'].str.strip() == nm_value.strip()) & 
                                        (matching_data[' TMK'].str.strip() == tmk_value.strip())]
                    
        if not filtered_result.empty:
            st.write(filtered_result)
        else:
            st.write("No matching rows found.")

def  perform_analysis_3(filtered_df):
    june_to_august_data = filtered_df[
        (filtered_df['MESS_DATUM'].dt.month >= 6) & (filtered_df['MESS_DATUM'].dt.month <= 8)
    ]
    analysis_df = june_to_august_data.copy()
    analysis_df['  NM'] = pd.to_numeric(analysis_df['  NM'], errors='coerce')
    analysis_df[' TMK'] = pd.to_numeric(analysis_df[' TMK'], errors='coerce')
    analysis_df['  FM'] = pd.to_numeric(analysis_df['  FM'], errors='coerce')
    analysis_df[' SDK'] = pd.to_numeric(analysis_df[' SDK'], errors='coerce')
    analysis_df.dropna(subset=['  FM'], inplace=True)

    if not analysis_df.empty:
        zero_NM_rows = analysis_df[(analysis_df['  NM'] == 0) | (analysis_df['  NM'] == 0.0)]
        ##st.write(zero_NM_rows)
        second_check = zero_NM_rows.nlargest(40,' TMK') 
        third_check = second_check.nlargest(20,' SDK')  
        fourth_check = third_check.nsmallest(5,'  FM')     

        st.success("Displaying details of 5 rows : ")
        processed_hottest_day = rename_columns(fourth_check)
        hottest_day_html = processed_hottest_day.to_html(index=False)
        st.markdown('<div class="scrolling-table">', unsafe_allow_html=True)
        st.markdown(hottest_day_html, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.warning("No data available for the selected date range.")


def  perform_analysis_2(filtered_df):
    analysis_df = filtered_df
    analysis_df['  NM'] = pd.to_numeric(analysis_df['  NM'], errors='coerce')
    analysis_df[' TMK'] = pd.to_numeric(analysis_df[' TMK'], errors='coerce')
    analysis_df['  FM'] = pd.to_numeric(analysis_df['  FM'], errors='coerce')
    analysis_df[' SDK'] = pd.to_numeric(analysis_df[' SDK'], errors='coerce')
    analysis_df.dropna(subset=['  FM'], inplace=True)

    if not analysis_df.empty:
        second_check = analysis_df.nlargest(50,' TMK')   
        third_check = second_check.nlargest(30,' SDK')     
        fourth_check = third_check.nsmallest(5, '  NM')

        st.success("Displaying details of 5 rows : ")
        processed_hottest_day = rename_columns(fourth_check)
        hottest_day_html = processed_hottest_day.to_html(index=False)
        st.markdown('<div class="scrolling-table">', unsafe_allow_html=True)
        st.markdown(hottest_day_html, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.warning("No data available for the selected date range.")


def  perform_analysis_1(filtered_df):
    analysis_df = filtered_df
    analysis_df[' TMK'] = pd.to_numeric(analysis_df[' TMK'], errors='coerce')
    analysis_df[' UPM'] = pd.to_numeric(analysis_df[' UPM'], errors='coerce')
    analysis_df['  FM'] = pd.to_numeric(analysis_df['  FM'], errors='coerce')
    
    if not analysis_df.empty:
        first_check = analysis_df.nlargest(20, ' TMK')
        second_check = first_check.nsmallest(5, '  FM')        
        third_check = second_check.nlargest(1, ' UPM')

        st.success("Displaying details 1 row : ")
        processed_hottest_day = rename_columns(third_check)
        hottest_day_html = processed_hottest_day.to_html(index=False)
        st.markdown('<div class="scrolling-table">', unsafe_allow_html=True)
        st.markdown(hottest_day_html, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.warning("No data available for the selected date range.")

def display_selected_data(data, year, month, day):
    # Convert the selected year, month, and day into a date
    selected_date = pd.to_datetime(f'{year}-{month}-{day}', format='%Y-%m-%d').date()

    selected_data = data[data['MESS_DATUM'].dt.date == selected_date]

    if not selected_data.empty:
        st.success("Climate Data for Date:")
        processed_selected_data  = rename_columns(selected_data)
        selected_data_html = processed_selected_data.to_html(index=False)
        ##st.markdown(selected_data_html, unsafe_allow_html=True)
        st.markdown('<div class="scrolling-table">', unsafe_allow_html=True)
        st.markdown(selected_data_html, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    else:
        st.warning("No data available for the selected date.")

if __name__ == '__main__':
    main()
