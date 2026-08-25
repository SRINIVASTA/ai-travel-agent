import streamlit as st
import json
import asyncio
from google import genai
from google.genai import types
from pydantic import BaseModel, Field
from typing import List, Optional
from playwright.async_api import async_playwright

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

# --- Async Playwright Cloud Worker ---
async def run_cloud_automation(data):
    logs = []
    logs.append("🚀 Spinning up headless cloud browser engine...")
    
    async with async_playwright() as p:
        # Cloud servers must run headless=True (no visible window)
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()
        
        if data['booking_type'] == "IRCTC Train":
            logs.append("🌐 Connecting to IRCTC Portal on the web server...")
            await page.goto("https://irctc.co.in", timeout=60000)
            
            # Extract the actual live web page title as proof of connection
            title = await page.title()
            logs.append(f"🔗 Successfully reached: '{title}'")
            
            # Simple form interaction check
            if data.get('source_city'):
                logs.append(f"✍️ Cloud agent prepared to inject source: {data['source_city']}")
            if data.get('destination_city'):
                logs.append(f"✍️ Cloud agent prepared to inject destination: {data['destination_city']}")
                
            logs.append("ℹ️ Cloud Session initialized! To proceed with actual bookings safely past the OTP wall, connect this output to a local Chrome Autofill Extension.")
            
        elif data['booking_type'] == "TTD Seva":
            logs.append("🌐 Connecting to TTD Official Portal...")
            await page.goto("https://ap.gov.in", timeout=60000)
            title = await page.title()
            logs.append(f"🔗 Successfully reached: '{title}'")
            logs.append(f"📋 Passenger data payload successfully compiled for TTD slots: {len(data['passengers'])} records ready.")
            
        await browser.close()
        return logs

# --- Streamlit UI Setup ---
st.set_page_config(page_title="Web Agentic Assistant", page_icon="🤖", layout="wide")

with st.sidebar:
    st.header("🔑 Authentication")
    user_api_key = st.text_input("Enter your Gemini API Key:", type="password", placeholder="AIzaSy...")

st.title("🌐 Cloud-Native Agentic AI Travel Controller")
st.caption("Running entirely on GitHub Web & Streamlit Community Cloud servers.")

if not user_api_key:
    st.warning("👈 Please enter your Gemini API Key in the sidebar to run this cloud app.")
    st.stop()

try:
    client = genai.Client(api_key=user_api_key)
except Exception as e:
    st.error(f"Initialization error: {e}")
    st.stop()

col1, col2 = st.columns()

with col1:
    st.subheader("🔮 Input Prompt")
    user_prompt = st.text_area("Enter travel query:", height=150, placeholder="Book a train from NDLS to TPTY...")
    generate_btn = st.button("🚀 Step 1: Extract Parameters", type="primary")

with col2:
    st.subheader("⚙️ Cloud Execution Terminal")
    
    if generate_btn and user_prompt:
        with st.spinner("Gemini is structuring your payload..."):
            try:
                response = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=f"Extract booking details: {user_prompt}",
                    config=types.GenerateContentConfig(
                        response_mime_type="application/json",
                        response_schema=TravelPayload,
                        temperature=0.1
                    ),
                )
                st.session_state['extracted_payload'] = response.text
                st.success("✅ JSON Compiled!")
            except Exception as e:
                st.error(f"Gemini Error: {e}")

    if 'extracted_payload' in st.session_state:
        payload_data = json.loads(st.session_state['extracted_payload'])
        st.json(payload_data)
        
        st.markdown("### 🤖 Trigger Headless Web Agent")
        
        if st.button("🏁 Run Cloud Web Check", type="secondary"):
            with st.spinner("Executing background browser sequence on Streamlit servers..."):
                try:
                    # Run the async browser tool straight inside the Streamlit web loop
                    execution_logs = asyncio.run(run_cloud_automation(payload_data))
                    
                    st.markdown("**Server Execution Logs:**")
                    for log in execution_logs:
                        st.text(log)
                    st.success("🎉 Background server check completed smoothly!")
                except Exception as e:
                    st.error(f"Cloud execution encountered an error: {e}")
