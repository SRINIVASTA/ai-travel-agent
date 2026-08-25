import streamlit as st
import json
import subprocess
import os
from google import genai
from google.genai import types
from pydantic import BaseModel, Field
from typing import List, Optional

# --- Define the Agent's Structured Output Schema ---
class Passenger(BaseModel):
    name: str = Field(description="Full name of the passenger")
    age: int = Field(description="Age of the passenger")
    gender: str = Field(description="Gender (Male/Female/Other)")

class TravelPayload(BaseModel):
    booking_type: str = Field(description="Must be either 'IRCTC Train' or 'TTD Seva'")
    source_city: Optional[str] = Field(None, description="Starting railway station code or city name")
    destination_city: Optional[str] = Field(None, description="Destination station code or city name")
    travel_date: str = Field(description="Date of travel/seva in YYYY-MM-DD format")
    preferred_slot: Optional[str] = Field(None, description="Morning, Afternoon, Evening, or Seva type if specified")
    passengers: List[Passenger] = Field(description="List of all traveling passengers extracted")

# --- Streamlit UI Setup ---
st.set_page_config(page_title="Agentic Travel Assistant", page_icon="🤖", layout="wide")

with st.sidebar:
    st.header("🔑 Authentication")
    user_api_key = st.text_input("Enter your Gemini API Key:", type="password", placeholder="AIzaSy...")
    st.markdown("---")
    st.markdown("### 💡 Quick Prompt Template")
    st.code("Book a train from NDLS to TPTY for 2026-10-15. Passengers: Rajesh Kumar, 45, Male and Sneha Kumar, 40, Female.")

st.title("🤖 Agentic AI Travel & Seva Controller")
st.caption("Converts unstructured chat requests into clean data payloads and commands a local browser automation grid.")

if not user_api_key:
    st.warning("👈 Please provide your Gemini API Key in the sidebar to start.")
    st.stop()

# Initialize Gemini Client
try:
    client = genai.Client(api_key=user_api_key)
except Exception as e:
    st.error(f"Failed to initialize Gemini Client: {e}")
    st.stop()

col1, col2 = st.columns()

with col1:
    st.subheader("🔮 Prompt Input")
    user_prompt = st.text_area("What are we booking today?", height=150, placeholder="Type your trip details...")
    generate_btn = st.button("🚀 Step 1: Extract Parameters", type="primary")

with col2:
    st.subheader("⚙️ Local Automation Control Panel")
    
    if generate_btn and user_prompt:
        with st.spinner("Gemini is extracting parameters into structured JSON..."):
            try:
                response = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=f"Extract the booking details from this prompt: {user_prompt}",
                    config=types.GenerateContentConfig(
                        response_mime_type="application/json",
                        response_schema=TravelPayload,
                        temperature=0.1
                    ),
                )
                
                st.session_state['extracted_payload'] = response.text
                st.success("✅ Parameters ready for execution!")
                
            except Exception as e:
                st.error(f"Gemini processing error: {e}")

    if 'extracted_payload' in st.session_state:
        st.json(st.session_state['extracted_payload'])
        
        st.markdown("### 🤖 Execute Local Browser Automator")
        st.info("Clicking below will spin up a visible local browser instance. It will fill out fields instantly, then halt at the checkpoint to let you solve the CAPTCHA manually.")
        
        if st.button("🏁 Run Playwright Script", type="secondary"):
            with st.spinner("Launching local automation worker..."):
                # Save data for the worker to read
                with open("payload.json", "w") as f:
                    f.write(st.session_state['extracted_payload'])
                
                # Run the background automation script
                result = subprocess.run(["python", "automation_worker.py"], capture_output=True, text=True)
                
                if result.returncode == 0:
                    st.success("🎉 Automation sequence completed!")
                else:
                    st.error(f"Worker closed or encountered an issue:\n{result.stderr}")
