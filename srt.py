import streamlit as st
import pandas as pd
import os

# Streamlit app title
st.title("XLSX to SRT Converter")

# Upload an XLSX file
xlsx_file = st.file_uploader("Upload an XLSX file", type=["xlsx"])

if xlsx_file:
    # Get the file name of the uploaded XLSX file
    xlsx_file_name = os.path.splitext(xlsx_file.name)[0]

    # Read the XLSX file with the first row as headers
    df = pd.read_excel(xlsx_file, header=None)

    # Combine all columns into a single 'Text' column
    df['Text'] = df.apply(lambda row: ' '.join(map(str, row)), axis=1)

    # Drop the original columns
    df = df[['Text']]

    # Initialize an empty list for SRT subtitles
    srt_subtitles = []

    # Iterate through the rows of the DataFrame
    for index, row in df.iterrows():
        # Extract text from the DataFrame
        text = row['Text']

        # Calculate timecode in SRT format (using zeros)
        start_time = "00:00:00,000"
        end_time = "00:00:00,000"

        # Create an SRT subtitle string
        subtitle = f"{index + 1}\n{start_time} --> {end_time}\n{text}\n"

        # Append the subtitle to the list
        srt_subtitles.append(subtitle)

    # Join the SRT subtitles into a single string
    srt_content = "\n".join(srt_subtitles)

    # Button to download the SRT file with the same name as the input XLSX file
    st.download_button(
        label=f"Download {xlsx_file_name}.srt",
        data=srt_content,
        key="download_srt",
        file_name=f"{xlsx_file_name}.srt",
    )
