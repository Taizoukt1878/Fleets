import streamlit as st
import requests
# from io import BytesIO
import json
# import os
# import time

# Set page configuration
st.set_page_config(
    page_title="Audio Processing App",
    page_icon="🎤",
    layout="wide"
)

# Constants
API_BASE_URL = "http://127.0.0.1:8081"  # Change this to your API's URL

def main():
    st.title("🎤 Audio Processing App")
    st.markdown("Upload an audio recording to transcribe and extract car data information.")
    
    # File uploader for audio
    uploaded_file = st.file_uploader("Choose an audio file", type=["wav", "mp3", "ogg"])
    
    # Container for results
    result_container = st.container()
    
    # Process audio when uploaded
    if uploaded_file is not None:
        with st.spinner("Processing audio..."):
            # Display audio player for the uploaded file
            st.audio(uploaded_file, format=f"audio/{uploaded_file.name.split('.')[-1]}")
            
            # Prepare the file for upload to the API
            files = {"audio_file": (uploaded_file.name, uploaded_file, f"audio/{uploaded_file.name.split('.')[-1]}")}
            
            try:
                # Send the file to the API
                response = requests.post(f"{API_BASE_URL}/upload_audio/", files=files)
                
                # Check if request was successful
                if response.status_code == 200:
                    data = response.json()
                    
                    # Display results
                    with result_container:
                        st.success("Audio processed successfully!")
                        
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.subheader("Audio Transcription")
                            st.write(data["transcribed_text"])
                        
                        with col2:
                            st.subheader("Car Data Analysis")
                            st.write(data["llm_response"])
                        
                        # Add download buttons for the results
                        export_data = {
                            "transcription": data["transcribed_text"],
                            "car_data": data["llm_response"]
                        }
                        
                        st.download_button(
                            label="Download Results as JSON",
                            data=json.dumps(export_data, indent=2),
                            file_name="audio_analysis_results.json",
                            mime="application/json"
                        )
                
                else:
                    st.error(f"Error: {response.status_code} - {response.text}")
            
            except Exception as e:
                st.error(f"Error connecting to API: {str(e)}")
                st.info("Make sure your FastAPI server is running at the specified URL.")

# Add a sidebar with settings
def sidebar():
    st.sidebar.title("Settings")
    
    # API endpoint configuration
    global API_BASE_URL
    API_BASE_URL = st.sidebar.text_input("API URL", API_BASE_URL)
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("### About")
    st.sidebar.info("""
    This app connects to a FastAPI backend to process audio files.
    The backend transcribes the audio and extracts car-related data.
    """)
    
    # API status indicator
    st.sidebar.markdown("### API Status")
    check_api_status()

def check_api_status():
    try:
        response = requests.get(f"{API_BASE_URL}/")
        if response.status_code == 200:
            st.sidebar.success("API is online")
        else:
            st.sidebar.error("API returned an error")
    except Exception as e:
        st.sidebar.error(f"API is offline{e}")

if __name__ == "__main__":
    sidebar()
    main()