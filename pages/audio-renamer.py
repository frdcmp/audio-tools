import streamlit as st
import pandas as pd
import os
from natsort import natsorted
import shutil
import zipfile

# Clean up any previous temporary files
shutil.rmtree("temp_renamed_files", ignore_errors=True)

# File uploader for audio files
uploaded_audio_files = st.file_uploader("Upload Audio files", type=["mp3", "wav", "ogg", "flac"], accept_multiple_files=True)

# File uploader for Excel file
uploaded_excel_file = st.file_uploader("Upload Excel file", type=["xlsx", "xls"])

# Function to create a dataframe
def create_dataframe(uploaded_excel_file, uploaded_audio_files):
    if uploaded_excel_file is None or uploaded_audio_files is None:
        return None

    # Save uploaded audio files to a temporary directory
    temp_audio_dir = "temp_audio_files"
    os.makedirs(temp_audio_dir, exist_ok=True)

    audio_files = []
    for file in uploaded_audio_files:
        file_name = os.path.join(temp_audio_dir, file.name)
        with open(file_name, "wb") as audio_file:
            audio_file.write(file.read())
        audio_files.append(file_name)

    excel_df = pd.read_excel(uploaded_excel_file)
    audio_df = pd.DataFrame({"Audio file names": audio_files})
    merged_df = pd.concat([audio_df, excel_df], axis=1)
    return merged_df

# Function to rename audio files and create a zip file
def rename_and_zip_files(merged_df, selected_column):
    temp_dir = "temp_renamed_files"
    os.makedirs(temp_dir, exist_ok=True)
    
    zip_filename = "renamed_audio_files.zip"
    zip_file_path = os.path.join(temp_dir, zip_filename)
    
    with zipfile.ZipFile(zip_file_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for index, row in merged_df.iterrows():
            audio_file_name = row["Audio file names"]
            if os.path.exists(audio_file_name):
                new_name = os.path.join(temp_dir, f"{row[selected_column]}.wav")
                os.rename(audio_file_name, new_name)
                zipf.write(new_name, os.path.basename(new_name))

    return zip_file_path

# Main app logic
if uploaded_excel_file is not None and uploaded_audio_files is not None:
    # Create a merged dataframe
    merged_df = create_dataframe(uploaded_excel_file, uploaded_audio_files)
    
    # Display the merged dataframe
    if merged_df is not None:
        st.write("Merged DataFrame:")
        st.dataframe(merged_df)

    # Dropdown menu for column selection
    selected_column = st.selectbox("Select a column to rename audio files:", merged_df.columns)
    
    if st.button("Rename and Download All"):
        if selected_column in merged_df.columns:
            zip_file_path = rename_and_zip_files(merged_df, selected_column)
            st.success("Audio files have been renamed successfully.")
            
            # Provide a button to download the zip file
            st.write("Download Renamed Files:")
            st.download_button(
                label="Download All Renamed Files",
                data=open(zip_file_path, "rb").read(),
                key="download_zip",
                file_name="renamed_audio_files.zip",
            )
        else:
            st.error("Please select a valid column.")

else:
    st.warning("Please upload an Excel file and audio files to get started.")
