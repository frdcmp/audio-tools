import streamlit as st
import pandas as pd
import os
from natsort import natsorted

# File uploader for Excel file
uploaded_file = st.file_uploader("Upload an Excel file", type=["xlsx", "xls"])

# Input field to specify the folder name within the 'audio' directory
folder_name = st.text_input("Enter the folder name within the 'audio' directory:", value="audio-renamer/")

# Function to scan audio files in the specified folder
def scan_audio_files(folder_name):
    audio_folder_path = os.path.join("audio", folder_name)
    if not os.path.exists(audio_folder_path):
        st.error(f"Folder '{folder_name}' does not exist in the 'audio' directory.")
        return None
    audio_files = [f for f in natsorted(os.listdir(audio_folder_path)) if f.lower().endswith(('.mp3', '.wav', '.ogg', '.flac'))]
    return audio_files

# Function to create a dataframe
def create_dataframe(uploaded_file, audio_files):
    if uploaded_file is None or audio_files is None:
        return None
    excel_df = pd.read_excel(uploaded_file)
    audio_df = pd.DataFrame({"Audio file names": audio_files})
    merged_df = pd.concat([audio_df, excel_df], axis=1)
    return merged_df

# Main app logic
if uploaded_file is not None:
    # Scan audio files with natural sorting
    audio_files = scan_audio_files(folder_name)
    
    # Create a merged dataframe
    merged_df = create_dataframe(uploaded_file, audio_files)
    
    # Display the merged dataframe
    if merged_df is not None:
        st.write("Merged DataFrame:")
        st.dataframe(merged_df)

    # Dropdown menu for column selection
    selected_column = st.selectbox("Select a column to rename audio files:", merged_df.columns)
    
    if st.button("Rename"):
        if selected_column in merged_df.columns:
            for index, row in merged_df.iterrows():
                audio_file_name = str(row["Audio file names"])
                old_name = os.path.join("audio", folder_name, audio_file_name)
                if os.path.exists(old_name):
                    new_name = os.path.join("audio", folder_name, f"{row[selected_column]}.wav")
                    os.rename(old_name, new_name)
                else:
                    st.warning(f"Audio file not found for the following row:\n\n{row.to_string()}\n\nSkipping rename for this file.")
            st.success("Audio files have been renamed successfully.")
        else:
            st.error("Please select a valid column.")



else:
    st.warning("Please upload an Excel file to get started.")
