import streamlit as st
from process_file import process_specific_data_file
from process_file import filter_specific_data_file
import pandas as pd

def specific_output_main():
    st.success('Welcome to Specific File Data Analysis')
    st.markdown('---')
    file = st.file_uploader("Upload File For Analysis")
    if file is not None:
        uploaded_file = process_specific_data_file(file)
        filtered_file = filter_specific_data_file(uploaded_file)

        unique_x_values = filtered_file['X (Grid)'].unique()
        unique_y_values = filtered_file['Y (Grid)'].unique()

        col1, col2 = st.columns(2)
        selected_x = col1.selectbox('Select X (Grid):', unique_x_values)
        selected_y = col2.selectbox('Select Y (Grid):', unique_y_values)

        selected_row = filtered_file[(filtered_file['X (Grid)'] == selected_x) & (filtered_file['Y (Grid)'] == selected_y)]
        st.markdown('---')
        st.success('Displaying Row with given Values of  (Grid) and Y (Grid)')
        selected_row_dataframe = pd.DataFrame(selected_row)
        selected_row_dataframe_reset = selected_row_dataframe.reset_index(drop=True)
        st.dataframe(selected_row_dataframe_reset)
        st.markdown('---')

        min_value = filtered_file['Data'].min()
        max_value = filtered_file['Data'].max()

        # Round the calculated mean, min, and max values to 3 decimal places
        mean_value1 = round(filtered_file['Data'].mean(), 3)
        min_value1 = round(filtered_file['Data'].min(), 3)
        max_value1 = round(filtered_file['Data'].max(), 3)

        # Display the rows corresponding to the calculated max value
        st.subheader(f'Rows with Max Value ({max_value1}):')
        max_rows = filtered_file[filtered_file['Data'] == max_value]
        max_dataframe = pd.DataFrame(max_rows)
        min_dataframe_reset = max_dataframe.reset_index(drop=True)
        st.dataframe(min_dataframe_reset)

        # Display the rows corresponding to the calculated min value
        st.subheader(f'Rows with Min Value ({min_value1}):')
        min_rows = filtered_file[filtered_file['Data'] == min_value]
        ##st.dataframe(min_rows)
        min_dataframe = pd.DataFrame(min_rows)
        min_dataframe_reset = min_dataframe.reset_index(drop=True)
        st.dataframe(min_dataframe_reset)

        # Display the rows corresponding to the calculated mean value
        st.subheader(f'Mean Value of Given Data: ({mean_value1})')
    else:
        st.warning('No file uploaded. Please upload a file for analysis.')
    