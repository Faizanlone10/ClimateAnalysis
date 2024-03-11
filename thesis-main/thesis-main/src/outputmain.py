import streamlit as st
from process_file import process_output_file,filter_output_file
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd


def calculate_and_display_mean_difference(main_data, additional_files, parameter_name):
    if additional_files[0] is not None and additional_files[1] is None:
        main_mean = main_data[parameter_name].mean()
        file_mean = additional_files[0][parameter_name].mean()
        mean_difference = abs(round(file_mean - main_mean, 2))
        st.success(f"Mean {parameter_name} Difference: {mean_difference}")

    elif additional_files[1] is not None:
        st.warning("Can't perform comparison analysis for more than 2 files")


def calculate_statistics(main_data, additional_files, parameter_name):
    main_stats = {}
    if main_data is not None:
        main_stats = {
            'Case Number': main_data['caseNumber'].iloc[0],
            'Mean': round(main_data[parameter_name].mean(), 2),
            'Min': round(main_data[parameter_name].min(), 2),
            'Max': round(main_data[parameter_name].max(), 2),
            'Standard Deviation': round(main_data[parameter_name].std(), 2)
        }

    file_stats = []
    for file_data in additional_files:
        if file_data is not None:
            stats = {
                'Case Number': file_data['caseNumber'].iloc[0],
                'Mean': round(file_data[parameter_name].mean(), 2),
                'Min': round(file_data[parameter_name].min(), 2),
                'Max': round(file_data[parameter_name].max(), 2),
                'Standard Deviation': round(file_data[parameter_name].std(), 2)
            }
            file_stats.append(stats)

    file_stats.append(main_stats)
    stats_df = pd.DataFrame(file_stats)
    return stats_df

def plot_wind_direction_line_chart(main_data, *additional_files):
    fig = go.Figure()
    if main_data is not None:
        fig.add_trace(go.Scatter(
            x=main_data['DateTime'],
            y=main_data['Wind Direction (deg)'],
            mode='lines',
            name=f"{main_data['caseNumber'].iloc[0]} at Height {main_data['topography'].iloc[0]}m",
            line=dict(color='blue')
        ))

    # Set contrasting colors for additional files
    contrast_colors = px.colors.qualitative.Light24[:len(additional_files)]

    for i, file_data in enumerate(additional_files):
        if file_data is not None:
            fig.add_trace(go.Scatter(
                x=file_data['DateTime'],
                y=file_data['Wind Direction (deg)'],
                mode='lines',
                name=f"{file_data['caseNumber'].iloc[0]} at Height {file_data['topography'].iloc[0]}m",
                line=dict(color=contrast_colors[i])
            ))

    fig.update_layout(
        xaxis=dict(title='DateTime'),
        yaxis=dict(title='Wind Direction (deg)'),
        legend=dict(x=1, y=1.1),  # Shift legend to top right
        title='Comparison of Wind Direction (deg) at Height (z)(m)'
    )

    st.plotly_chart(fig)
    calculate_and_display_mean_difference(main_data, additional_files, 'Wind Direction (deg)')
    statistics_table = calculate_statistics(main_data, additional_files, 'Wind Direction (deg)')
    st.dataframe(statistics_table)
 

def plot_radiance_line_chart(main_data, *additional_files):
    fig = go.Figure()
    if main_data is not None:
        fig.add_trace(go.Scatter(
            x=main_data['DateTime'],
            y=main_data['Mean Radiant Temperature (°C)'],
            mode='lines',
            name=f"{main_data['caseNumber'].iloc[0]} at Height {main_data['topography'].iloc[0]}m",
            line=dict(color='blue')
        ))

    # Set contrasting colors for additional files
    contrast_colors = px.colors.qualitative.Light24[:len(additional_files)]

    for i, file_data in enumerate(additional_files):
        if file_data is not None:
            fig.add_trace(go.Scatter(
                x=file_data['DateTime'],
                y=file_data['Mean Radiant Temperature (°C)'],
                mode='lines',
                name=f"{file_data['caseNumber'].iloc[0]} at Height {file_data['topography'].iloc[0]}m",
                line=dict(color=contrast_colors[i])
            ))

    fig.update_layout(
        xaxis=dict(title='DateTime'),
        yaxis=dict(title='Mean Radiant Temperature (°C)'),
        legend=dict(x=1, y=1.1),  # Shift legend to top right
        title='Comparison of Mean Radiant Temperature at Height (z)(m)'
    )

    st.plotly_chart(fig)
    calculate_and_display_mean_difference(main_data, additional_files, 'Mean Radiant Temperature (°C)')
    statistics_table = calculate_statistics(main_data, additional_files, 'Mean Radiant Temperature (°C)')
    st.dataframe(statistics_table)
    

def plot_humidity_line_chart(main_data, *additional_files):
    fig = go.Figure()

    if main_data is not None:
        fig.add_trace(go.Scatter(
            x=main_data['DateTime'],
            y=main_data['Specific Humidity (g/kg)'],
            mode='lines',
            name=f"{main_data['caseNumber'].iloc[0]} at Height {main_data['topography'].iloc[0]}m",
            line=dict(color='blue')
        ))

    # Set contrasting colors for additional files
    contrast_colors = px.colors.qualitative.Light24[:len(additional_files)]

    for i, file_data in enumerate(additional_files):
        if file_data is not None:
            fig.add_trace(go.Scatter(
                x=file_data['DateTime'],
                y=file_data['Specific Humidity (g/kg)'],
                mode='lines',
                name=f"{file_data['caseNumber'].iloc[0]} at Height {file_data['topography'].iloc[0]}m",
                line=dict(color=contrast_colors[i])
            ))

    fig.update_layout(
        xaxis=dict(title='DateTime'),
        yaxis=dict(title='Specific Humidity (g/kg)'),
        legend=dict(x=1, y=1.1),  # Shift legend to top right
        title='Comparison of Specific Humidity at Height (z)(m)'
    )

    st.plotly_chart(fig)
    calculate_and_display_mean_difference(main_data, additional_files, 'Specific Humidity (g/kg)')
    statistics_table = calculate_statistics(main_data, additional_files, 'Specific Humidity (g/kg)')
    st.dataframe(statistics_table)



def plot_windSpeed_line_chart(main_data, *additional_files):
    fig = go.Figure()

    if main_data is not None:
        fig.add_trace(go.Scatter(
            x=main_data['DateTime'],
            y=main_data['wSpeed (m/s)'],
            mode='lines',
            name=f"{main_data['caseNumber'].iloc[0]} at Height {main_data['topography'].iloc[0]}m",
            line=dict(color='blue')
        ))

    # Set contrasting colors for additional files
    contrast_colors = px.colors.qualitative.Light24[:len(additional_files)]

    for i, file_data in enumerate(additional_files):
        if file_data is not None:
            fig.add_trace(go.Scatter(
                x=file_data['DateTime'],
                y=file_data['wSpeed (m/s)'],
                mode='lines',
                name=f"{file_data['caseNumber'].iloc[0]} at Height {file_data['topography'].iloc[0]}m",
                line=dict(color=contrast_colors[i])
            ))

    fig.update_layout(
        xaxis=dict(title='DateTime'),
        yaxis=dict(title='Wind Speed (m/s)'),
        legend=dict(x=1, y=1.1),  # Shift legend to top right
        title='Comparison of Wind Speed at Height (z)(m)'
    )

    st.plotly_chart(fig)
    calculate_and_display_mean_difference(main_data, additional_files, 'wSpeed (m/s)')
    statistics_table = calculate_statistics(main_data, additional_files, 'wSpeed (m/s)')
    st.dataframe(statistics_table)


def plot_temperature_line_chart(main_data, *additional_files):
    fig = go.Figure()

    if main_data is not None:
        fig.add_trace(go.Scatter(
            x=main_data['DateTime'],
            y=main_data[' Potential Air Temperature (°C)'],
            mode='lines',
            name=f"{main_data['caseNumber'].iloc[0]} at Height {main_data['topography'].iloc[0]}m",
            line=dict(color='blue')
        ))

    # Set contrasting colors for additional files
    contrast_colors = px.colors.qualitative.Light24[:len(additional_files)]

    for i, file_data in enumerate(additional_files):
        if file_data is not None:
            fig.add_trace(go.Scatter(
                x=file_data['DateTime'],
                y=file_data[' Potential Air Temperature (°C)'],
                mode='lines',
                name=f"{file_data['caseNumber'].iloc[0]} at Height {file_data['topography'].iloc[0]}m",
                line=dict(color=contrast_colors[i])
            ))

    fig.update_layout(
        xaxis=dict(title='DateTime'),
        yaxis=dict(title='Potential Air Temperature (°C)'),
        legend=dict(x=1, y=1.1),  # Shift legend to top right
        title='Comparison of Potential Air Temperature at Height (z)(m)'
    )

    st.plotly_chart(fig)

    calculate_and_display_mean_difference(main_data, additional_files, ' Potential Air Temperature (°C)')
    statistics_table = calculate_statistics(main_data, additional_files, ' Potential Air Temperature (°C)')
    st.dataframe(statistics_table)
        

def display_z_option(analysis_values, instance_number):
    unique_values = analysis_values['z (m)'].unique()
    
    selectbox_key = f"select_z_m_value_{instance_number}"
    
    topography_height = None
    col1, col2 = st.columns(2)
    with col1:
        selected_value = st.selectbox(f"Select a value of Height you want to do Analysis at for File {instance_number}", unique_values, key=selectbox_key)
    with col2:
        if selected_value:
            input_key = f"topography_input_{instance_number}"  # Unique key for the input
            entered_height = st.number_input("Enter Topography height (less than selected value):", key=input_key)

            if entered_height is not None and isinstance(entered_height, (int, float)):
                if isinstance(selected_value, (int, float)) and entered_height < selected_value:
                    topography_height = selected_value - entered_height
                    topography_height = round(topography_height, 2)
                else:
                    st.error("Invalid input. Please ensure the entered height is a number and less than the selected value.")
            else:
                st.error("Invalid input. Please enter a numeric value.")
    st.write("You selected: ", selected_value,"m  |" " Topography Height: ", entered_height,"m")
    return selected_value, topography_height

def output_main():
    st.success('Welcome to Output File Data Analysis')
    st.markdown('---')
    main_case_number = st.text_input("Enter file comments")
    main_file_0 = st.file_uploader("Upload Main File To Do Comparison")
    main_file = process_output_file(main_file_0)
    
    if main_file is not None:
        main_file['caseNumber'] = main_case_number if main_case_number else None
        
        unique_z_values = main_file['z (m)'].unique()
        
        ##st.write("Unique values in 'z (m)' column(without 'in terrain' values):")
        ##st.dataframe(pd.DataFrame(unique_z_values, columns=['Unique z (m)']).T)
        topography_height = None
        col1, col2 = st.columns(2)
        with col1:
            selected_z_value = st.selectbox("Select a value of Height(m) you want to do Analysis at", unique_z_values)

        with col2:
            entered_height = None
            if selected_z_value:
                entered_height = st.number_input("Enter Topography height (less than selected value):")

            if entered_height is not None and isinstance(entered_height, (int, float)):
                if isinstance(selected_z_value, (int, float)) and entered_height < selected_z_value:
                    topography_height = selected_z_value - entered_height
                    topography_height = round(topography_height, 2)
                else:
                    st.error("Invalid input. Please ensure the entered height is a number and less than the selected value.")
            else:
                st.error("Invalid input. Please enter a numeric value.")

        main_file['topography'] = topography_height if topography_height else None
        st.write("You selected: ", selected_z_value,"m  |" " Topography Height: ", entered_height,"m")
        st.markdown('---')
        
        filtered_main_file = filter_output_file(main_file, selected_z_value)

    num_additional_files = st.number_input("Enter the number of additional files to upload (max 10)", min_value=1, max_value=10, value=1)
    # Declare variables before the loop
    analysis_file_1 = None
    analysis_file_2 = None
    analysis_file_3 = None
    analysis_file_4 = None
    analysis_file_5 = None
    analysis_file_6 = None
    analysis_file_7 = None
    analysis_file_8 = None
    analysis_file_9 = None
    analysis_file_10 = None

    for i in range(num_additional_files):
        st.markdown('---')
        case_number = st.text_input(f"Enter comments for file {i+1}")
        uploaded_file = st.file_uploader(f"Upload Additional File {i+1}")
        if uploaded_file is not None:
            # Assign uploaded files to variables
            if i == 0:
                file_1 = uploaded_file
                analysis_1 = process_output_file(file_1)
                
                selected_1_value, topography_height_1 = display_z_option(analysis_1,1)
                analysis_1['topography'] = topography_height_1 if topography_height_1 else None

                analysis_file_1 = filter_output_file(analysis_1, selected_1_value)
                analysis_file_1['caseNumber'] = case_number if case_number else None
            elif i == 1:
                file_2 = uploaded_file
                analysis_2 = process_output_file(file_2)

                selected_2_value, topography_height_2 = display_z_option(analysis_2,2)
                analysis_2['topography'] = topography_height_2 if topography_height_2 else None

                analysis_file_2 = filter_output_file(analysis_2, selected_2_value)
                analysis_file_2['caseNumber'] = case_number if case_number else None
            elif i == 2:
                file_3 = uploaded_file
                analysis_3 = process_output_file(file_3)

                selected_3_value, topography_height_3 = display_z_option(analysis_3,3)
                analysis_3['topography'] = topography_height_3 if topography_height_3 else None

                analysis_file_3 = filter_output_file(analysis_3, selected_3_value)
                analysis_file_3['caseNumber'] = case_number if case_number else None
            elif i == 3:
                file_4 = uploaded_file
                analysis_4 = process_output_file(file_4)

                selected_4_value, topography_height_4 = display_z_option(analysis_4,4)
                analysis_4['topography'] = topography_height_4 if topography_height_4 else None

                analysis_file_4 = filter_output_file(analysis_4, selected_4_value)
                analysis_file_4['caseNumber'] = case_number if case_number else None
            elif i == 4:
                file_5 = uploaded_file
                analysis_5 = process_output_file(file_5)

                selected_5_value, topography_height_5 = display_z_option(analysis_5,5)
                analysis_5['topography'] = topography_height_5 if topography_height_5 else None

                analysis_file_5 = filter_output_file(analysis_5, selected_5_value)
                analysis_file_5['caseNumber'] = case_number if case_number else None
            elif i == 5:
                file_6 = uploaded_file
                analysis_6 = process_output_file(file_6)

                selected_6_value, topography_height_6 = display_z_option(analysis_6,6)
                analysis_6['topography'] = topography_height_6 if topography_height_6 else None

                analysis_file_6 = filter_output_file(analysis_6, selected_6_value)
                analysis_file_6['caseNumber'] = case_number if case_number else None
            elif i == 6:
                file_7 = uploaded_file
                analysis_7 = process_output_file(file_7)

                selected_7_value, topography_height_7 = display_z_option(analysis_7,7)
                analysis_7['topography'] = topography_height_7 if topography_height_7 else None

                analysis_file_7 = filter_output_file(analysis_7, selected_7_value)
                analysis_file_7['caseNumber'] = case_number if case_number else None
            elif i == 7:
                file_8 = uploaded_file
                analysis_8 = process_output_file(file_8)

                selected_8_value, topography_height_8 = display_z_option(analysis_8,8)
                analysis_8['topography'] = topography_height_8 if topography_height_8 else None

                analysis_file_8 = filter_output_file(analysis_8, selected_8_value)
                analysis_file_8['caseNumber'] = case_number if case_number else None
            elif i == 8:
                file_9 = uploaded_file
                analysis_9 = process_output_file(file_9)

                selected_9_value, topography_height_9 = display_z_option(analysis_9,9)
                analysis_9['topography'] = topography_height_9 if topography_height_9 else None

                analysis_file_9 = filter_output_file(analysis_9, selected_9_value)
                analysis_file_9['caseNumber'] = case_number if case_number else None
            elif i == 9:
                file_10 = uploaded_file
                analysis_10 = process_output_file(file_10)

                selected_10_value, topography_height_10 = display_z_option(analysis_10,10)
                analysis_10['topography'] = topography_height_10 if topography_height_10 else None

                analysis_file_10 = filter_output_file(analysis_10, selected_10_value)
                analysis_file_10['caseNumber'] = case_number if case_number else None
    
    st.markdown('---')
    col1, col2, col3, col4, col5 = st.columns(5)
    if col1.button("Temperature"):  
        plot_temperature_line_chart(filtered_main_file, analysis_file_1, analysis_file_2, analysis_file_3, analysis_file_4, analysis_file_5, analysis_file_6, analysis_file_7, analysis_file_8, analysis_file_9, analysis_file_10)
    if col2.button("Wind Speed"):
        plot_windSpeed_line_chart(filtered_main_file, analysis_file_1, analysis_file_2, analysis_file_3, analysis_file_4, analysis_file_5, analysis_file_6, analysis_file_7, analysis_file_8, analysis_file_9, analysis_file_10)
    if col3.button("Humidity"):
        plot_humidity_line_chart(filtered_main_file, analysis_file_1, analysis_file_2, analysis_file_3, analysis_file_4, analysis_file_5, analysis_file_6, analysis_file_7, analysis_file_8, analysis_file_9, analysis_file_10)
    if col4.button("Mean Radiance"):
        plot_radiance_line_chart(filtered_main_file, analysis_file_1, analysis_file_2, analysis_file_3, analysis_file_4, analysis_file_5, analysis_file_6, analysis_file_7, analysis_file_8, analysis_file_9, analysis_file_10)
    if col5.button("Wind Direction"):
        plot_wind_direction_line_chart(filtered_main_file, analysis_file_1, analysis_file_2, analysis_file_3, analysis_file_4, analysis_file_5, analysis_file_6, analysis_file_7, analysis_file_8, analysis_file_9, analysis_file_10)

 
