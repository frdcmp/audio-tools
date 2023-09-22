import streamlit as st
import pandas as pd
from io import BytesIO
import re

# Function to parse VTT and convert it to a DataFrame
def vtt_to_dataframe(vtt_text):
    lines = vtt_text.split('\n')
    data = []
    start_time, end_time = None, None

    for line in lines:
        # Use regular expression to match timestamps and text
        timestamp_match = re.match(r'(\d{2}:\d{2}:\d{2}.\d{3}) --> (\d{2}:\d{2}:\d{2}.\d{3})', line)
        if timestamp_match:
            start_time, end_time = timestamp_match.groups()
        elif line.strip() and start_time is not None and end_time is not None:
            data.append([start_time, end_time, line])

    df = pd.DataFrame(data, columns=['Start Time', 'End Time', 'Text'])
    return df

# Streamlit app
st.title("VTT to Excel Converter")

uploaded_vtt = st.file_uploader("Upload a VTT file", type=["vtt"])

if uploaded_vtt is not None:
    vtt_text = uploaded_vtt.read().decode('utf-8')
    df = vtt_to_dataframe(vtt_text)

    st.subheader("VTT Data in DataFrame:")
    st.dataframe(df)

    # Convert to Excel
    st.subheader("Download Excel")
    excel_buffer = BytesIO()
    df.to_excel(excel_buffer, index=False, engine='openpyxl')
    excel_buffer.seek(0)
    st.download_button(
        label="Download as XLSX",
        data=excel_buffer,
        key='xlsx',
        file_name='vtt_data.xlsx',
    )
