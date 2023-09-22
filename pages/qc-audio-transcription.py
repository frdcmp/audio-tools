import os
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import librosa.display
from pydub import AudioSegment
import whisper

# Function to list audio files in the './audio' folder and return a DataFrame
def list_audio_files(folder_path='./audio'):
    audio_files = [file for file in os.listdir(folder_path) if file.endswith('.wav')]
    df = pd.DataFrame({'Audio Files': audio_files})
    return df

# Function to load and plot the waveform of the selected audio file
def plot_audio_waveform(audio_path):
    plt.figure(figsize=(10, 4))
    y, sr = librosa.load(audio_path)
    librosa.display.waveshow(y, sr=sr)
    plt.title('Audio Waveform')
    plt.xlabel('Time (seconds)')
    plt.ylabel('Amplitude')
    return plt

# Function to play the selected audio file
def play_audio(audio_path):
    audio = AudioSegment.from_wav(audio_path)
    audio.export("temp.wav", format="wav")
    st.audio("temp.wav", format="audio/wav")

# Function to transcribe the selected audio file using OpenAI Whisper
def transcribe_audio(audio_path, model_name='base'):
    model = whisper.load_model(model_name)
    result = model.transcribe(audio_path)
    text = result['text']
    return text


def main():
    st.title('Audio Visualization App')

    # List audio files in a DataFrame
    audio_df = list_audio_files()
    st.subheader('Audio Files')
    st.dataframe(audio_df)

    # Create or get the session state
    if 'selected_index' not in st.session_state:
        st.session_state.selected_index = 0

    # Dropdown to select the audio file
    selected_audio = st.selectbox('Select an Audio File', audio_df['Audio Files'], index=st.session_state.selected_index)

    # Dropdown to select the Whisper model
    model_options = ["tiny", "base", "small", "medium", "large"]
    selected_model = st.selectbox('Select a Whisper Model', model_options, index=2)

    # Add a "Next Audio File" button
    next_button = st.button("Next Audio File")

    # Handle button click and update the selected index
    if next_button:
        st.session_state.selected_index = (st.session_state.selected_index + 1) % len(audio_df)

    # Get the current selected audio based on the updated index
    selected_audio = audio_df['Audio Files'][st.session_state.selected_index]

    # Plot the audio waveform, play the audio, and display the transcription result
    if selected_audio and selected_model:
        audio_path = os.path.join('./audio', selected_audio)
        fig = plot_audio_waveform(audio_path)
        st.subheader('Audio Waveform')
        st.pyplot(fig)

        st.subheader('Audio Player')
        play_audio(audio_path)

        transcription_text = transcribe_audio(audio_path, selected_model)
        st.subheader('Transcription Result')
        st.write(transcription_text)

if __name__ == "__main__":
    main()