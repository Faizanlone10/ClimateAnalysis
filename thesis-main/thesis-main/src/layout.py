import streamlit as st

def set_page_layout():
    """
    Set the layout and style for the Streamlit page.
    """
    # Set the page title and favicon (if needed)
    st.set_page_config(
        page_title="Climate Data App",
        page_icon="🌦️",
        layout="wide",  # Use a wide layout
    )

    # Custom CSS to change the background color, font alignment, and font styling
    st.markdown(
        f"""
        <style>
        body {{
            background: #cfe2d4; /* Light green background color for the entire page */
        }}
        .reportview-container {{
             background: transparent;
            text-align: left;
            font-size: 14px; /* Reduce font size */
            font-family: 'Arial', sans-serif;
            color: #333; /* Dark gray font color */
        }}
        table {{
            border-collapse: collapse;
            width: 50%;
            max-width: 50%; /* Reduce the maximum width of the table */
            font-size: 12px; /* Reduce font size within the table */
        }}
        th, td {{
            text-align: left;
            padding: 4px; /* Reduce padding */
        }}
        tr:nth-child(even) {{
            background-color: #e7e7e7; /* Lighter gray alternate row color */
        }}
        th {{
            background-color: #4CAF50; /* Green header row color */
            color: white;
        }}
        .stButton button {{
            background-color: red; /* Red button color */
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )

    # Rest of your code remains unchanged

# Rest of your code remains unchanged
