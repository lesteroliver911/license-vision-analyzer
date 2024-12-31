import os
import streamlit as st
import google.generativeai as genai
from PIL import Image
import io
import logging
from dotenv import load_dotenv
import base64
from typing import Optional

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Get API key from environment variables
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("Missing required GEMINI_API_KEY in environment variables")

# Configure Gemini API
genai.configure(api_key=GEMINI_API_KEY)

# Initialize the Gemini model with flash thinking configuration
# Generation configuration from google-flash-thinking.py
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

def initialize_model():
    """Initialize the Gemini model with configurations"""
    try:
        model = genai.GenerativeModel(
            model_name="gemini-2.0-flash-thinking-exp-1219",
            generation_config=generation_config,
        )
        return model
    except Exception as e:
        logger.error(f"Failed to initialize Gemini model: {e}")
        raise

def process_image(image_file) -> Optional[Image.Image]:
    """Process the uploaded image file"""
    try:
        image = Image.open(image_file)
        # Convert to RGB if necessary
        if image.mode != 'RGB':
            image = image.convert('RGB')
        return image
    except Exception as e:
        logger.error(f"Error processing image: {e}")
        return None

def analyze_license(model, image: Image.Image, custom_prompt: str):
    """Analyze the driver's license using Gemini model"""
    try:
        chat = model.start_chat(history=[])
        
        # Combine custom prompt with base instructions
        full_prompt = f"""
        Please analyze this driver's license image and {custom_prompt}
        
        Please provide the information in a clear, structured format.
        If any information is unclear or cannot be read, please indicate that.
        """
        
        # Create message with image and text
        response = chat.send_message([
            full_prompt,
            image
        ])
        
        return response.text
    except Exception as e:
        logger.error(f"Error analyzing license: {e}")
        raise

def main():
    st.set_page_config(
        page_title="Driver's License Analyzer",
        page_icon="🪪",
        layout="wide"
    )
    
    # Sidebar for upload and preview only
    with st.sidebar:
        uploaded_file = st.file_uploader(
            "Choose a driver's license image",
            type=['jpg', 'jpeg', 'png'],
            help="Upload a clear image of the driver's license"
        )
        
        # Show preview in sidebar if image is uploaded
        if uploaded_file:
            try:
                image = process_image(uploaded_file)
                if image:
                    st.subheader("License Preview")
                    st.image(image, caption="Uploaded License", use_container_width=True)
            except Exception as e:
                st.error(f"Error: {str(e)}")

        # Keep usage instructions in sidebar bottom
        with st.expander("ℹ️ How to Use"):
            st.markdown("""
            1. Upload a clear image of a driver's license using the file uploader
            2. Enter custom instructions for what information you want to extract
            3. Preview the uploaded image to ensure it's clear and readable
            4. Click 'Analyze License' to process the image
            5. View the results and download them if needed
            
            **Note:** Ensure the license image is:
            - Clear and well-lit
            - All text is readable
            - No glare or reflections
            - Complete (no cut-off edges)
            """)

    # Main content area
    # Removed st.title("Driver's License Analysis")
    
    # Initialize model
    try:
        model = initialize_model()
    except Exception as e:
        st.error(f"Error initializing model: {str(e)}")
        return

    # Move custom prompt to main area
    custom_prompt = st.text_area(
        "Custom Analysis Instructions",
        placeholder="Example: extract the name, date of birth, and expiration date",
        help="Specify what information you want to extract from the license"
    )

    # Analysis section in main area
    if uploaded_file and custom_prompt:
        if st.button("Analyze License"):
            with st.spinner("Analyzing license..."):
                try:
                    image = process_image(uploaded_file)
                    if image:
                        analysis = analyze_license(model, image, custom_prompt)
                        
                        st.subheader("Analysis Results")
                        st.markdown(analysis)
                        
                        # Add download button for results
                        result_str = f"""
                        Driver's License Analysis Results
                        --------------------------------
                        
                        {analysis}
                        """
                        b64 = base64.b64encode(result_str.encode()).decode()
                        href = f'<a href="data:text/plain;base64,{b64}" download="license_analysis.txt">Download Analysis Results</a>'
                        st.markdown(href, unsafe_allow_html=True)
                        
                except Exception as e:
                    st.error(f"Error during analysis: {str(e)}")
    else:
        if not uploaded_file:
            st.info("👈 Upload a driver's license image in the sidebar to begin")
        elif not custom_prompt:
            st.info("✍️ Please provide analysis instructions above")

if __name__ == "__main__":
    main()
