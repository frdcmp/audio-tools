import streamlit as st

# Title for your Streamlit app
st.title("VTT to SRT Converter")

# Upload a VTT file
uploaded_file = st.file_uploader("Choose a VTT file", type=["vtt"])

if uploaded_file is not None:
    # Read the uploaded VTT file
    vtt_content = uploaded_file.read().decode('utf-8')

    # Split the VTT content into captions
    captions = vtt_content.strip().split('\n\n')

    # Convert to SRT format
    srt_content = ""
    for idx, caption in enumerate(captions):
        caption_lines = caption.strip().split('\n')
        if len(caption_lines) >= 3:
            caption_start = caption_lines[0]
            caption_time, caption_text = caption_lines[1], caption_lines[2]
            srt_content += f"{idx + 1}\n"
            srt_content += f"{caption_start.replace('.', ',')}0 --> {caption_time.replace('.', ',')}0\n"
            srt_content += f"{caption_text}\n\n"

    # Display the converted SRT content
    st.write("Converted SRT content:")
    st.text_area("SRT Content", srt_content, height=400)
