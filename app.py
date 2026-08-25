import streamlit as st
import json
import datetime
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
st.set_page_config(page_title="Web Agentic Assistant", page_icon="🤖", layout="wide")

with st.sidebar:
    st.header("🔑 Authentication")
    user_api_key = st.text_input("Enter your Gemini API Key:", type="password", placeholder="AIzaSy...")
    st.markdown("---")
    st.markdown("### 📋 Active System State")
    st.success("⚡ Engine Status: Online (Cloud Optimized)")

st.title("🌐 Cloud-Native Agentic AI Travel Controller")
st.caption("Running seamlessly on Streamlit Community Cloud — Built for zero-error web execution.")

if not user_api_key:
    st.warning("👈 Please enter your Gemini API Key in the sidebar to open the workspace.")
    st.stop()

try:
    client = genai.Client(api_key=user_api_key)
except Exception as e:
    st.error(f"Initialization error: {e}")
    st.stop()

# Explicitly passing '2' to create 2 columns safely in the latest Streamlit core engine
col1, col2 = st.columns(2)

with col1:
    st.subheader("🔮 Conversational Input")
    user_prompt = st.text_area(
        "Enter booking requirements:", 
        height=150, 
        placeholder="Example: Book a train from NDLS to TPTY for today. Passenger: Ravi, 34, Male."
    )
    generate_btn = st.button("🚀 Process via Agent Brain", type="primary")

with col2:
    st.subheader("⚙️ Agentic Handoff Terminal")
    
    if generate_btn and user_prompt:
        with st.spinner("Gemini is structuring your payload..."):
            try:
                # Capture today's calendar date straight from the cloud server environment
                today_str = datetime.date.today().strftime("%Y-%m-%d")
                
                # Dynamic Instruction Anchor Framework for relative date context calculations
                prompt_context = f"""
                Today's absolute baseline date is: {today_str}.
                Using this absolute anchor date, calculate and extract the correct calendar dates from the user prompt text.
                
                Rules for relative dates:
                - If the user writes 'today', map the travel_date to exactly '{today_str}'
                - If the user writes 'tomorrow', calculate the next day relative to '{today_str}'
                - Calculate any relative days of the week (e.g., 'next Friday') starting forward from '{today_str}'
                
                User Prompt Payload: {user_prompt}
                """
                
                response = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=prompt_context,
                    config=types.GenerateContentConfig(
                        response_mime_type="application/json",
                        response_schema=TravelPayload,
                        temperature=0.1
                    ),
                )
                st.session_state['extracted_payload'] = response.text
                st.success("✅ JSON Payload Generated Successfully!")
            except Exception as e:
                st.error(f"Gemini Processing Error: {e}")

    if 'extracted_payload' in st.session_state:
        payload_data = json.loads(st.session_state['extracted_payload'])
        st.json(payload_data)
        
        st.markdown("### 🧭 Portal Quick Navigation")
        
        if payload_data['booking_type'] == "IRCTC Train":
            target_url = "https://irctc.co.in"
            st.info(f"🚄 **AI Recommendation:** Target Route: **{payload_data['source_city']} ➔ {payload_data['destination_city']}** scheduled for **{payload_data['travel_date']}**")
        else:
            target_url = "https://ap.gov.in"
            st.info(f"🛕 **AI Recommendation:** Headed to TTD Portal for Darshan slots scheduled for **{payload_data['travel_date']}**")
            
        st.link_button(f"🔗 Open Official {payload_data['booking_type']} Website", target_url, type="primary")
        
        # Optimized copyable block for the web-only bookmarklet macro tool
        st.markdown("#### 📋 Web-Agent Injection Payload")
        st.caption("Click the copy button in the top right of the box below, then trigger your browser bookmarklet on the target booking page:")
        injection_string = json.dumps(payload_data)
        st.code(injection_string, language="json")
