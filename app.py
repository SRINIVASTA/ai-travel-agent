import streamlit as st
import json
import datetime
from google import genai
from google.genai import types
from pydantic import BaseModel, Field
from typing import List, Optional

# --- Define the Agent's Master Structured Output Schema ---
class Passenger(BaseModel):
    name: str = Field(description="Full name of the person as per ID proof")
    age: int = Field(description="Age of the person in years")
    gender: str = Field(description="Gender of the person. Must be exactly 'Male', 'Female', or 'Transgender'")
    identity_proof_type: str = Field(description="Type of ID Proof. Must be 'Aadhaar Card' for Indian residents or 'Passport' for international travelers.")
    photo_identity_type: str = Field(description="Photo identification type. Must match identity_proof_type exactly (either 'Aadhaar Card' or 'Passport').")
    identity_number: str = Field(description="The unique 12-digit Aadhaar number or alphanumeric Passport number.")
    mobile_no: str = Field(description="Primary 10-digit mobile contact number of the passenger.")
    city: str = Field(description="City or town of residence.")
    state: str = Field(description="State or province of residence.")
    country: str = Field(default="India", description="Country of residence.")
    pincode: str = Field(description="6-digit postal pincode (or zip code for foreign nationals).")

class TravelPayload(BaseModel):
    booking_type: str = Field(description="Must be either 'IRCTC Train' or 'TTD Seva'")
    source_city: Optional[str] = Field(None, description="Starting railway station code or city name")
    destination_city: Optional[str] = Field(None, description="Destination station code or city name")
    travel_date: str = Field(description="Date of travel/seva in YYYY-MM-DD format")
    preferred_slot: Optional[str] = Field(None, description="Morning, Afternoon, Evening, or Seva type if specified")
    passengers: List[Passenger] = Field(description="Comprehensive list of all traveling passengers containing complete identity pairings, contact records, and address details.")

# --- Streamlit UI Setup ---
st.set_page_config(page_title="Web Agentic Assistant", page_icon="🤖", layout="wide")

with st.sidebar:
    st.header("🔑 Authentication")
    user_api_key = st.text_input("Enter your Gemini API Key:", type="password", placeholder="AIzaSy...")
    st.markdown("---")
    st.markdown("### 📋 Active System State")
    st.success("⚡ Master Engine: Full Core KYC & Gender Inclusive Parser Online")

st.title("🌐 Cloud-Native Agentic AI Travel Controller")
st.caption("Running seamlessly on Streamlit Community Cloud — Fully supports Name, Age, Male/Female/Transgender options, Aadhaar/Passport tracking, Addresses, and Contacts.")

if not user_api_key:
    st.warning("👈 Please enter your Gemini API Key in the sidebar to open the workspace.")
    st.stop()

try:
    client = genai.Client(api_key=user_api_key)
except Exception as e:
    st.error(f"Initialization error: {e}")
    st.stop()

# Create 2 columns safely in the latest Streamlit core engine
col1, col2 = st.columns(2)

# --- COLUMN 1: INPUT AND EASY COPY PASTE ZONE ---
with col1:
    st.subheader("🔮 Conversational Input")
    user_prompt = st.text_area(
        "Enter booking requirements:", 
        height=220, 
        placeholder="Example: Book TTD Seva for tomorrow. Passenger 1: Kiran Sharma, 31, Transgender, Aadhaar: 111122223333, Mobile: 9898989898, living in New Delhi, Delhi, Pincode 110001."
    )
    generate_btn = st.button("🚀 Process via Agent Brain", type="primary")

    # The payload is positioned down here directly under the execution button for quick copy access
    if 'extracted_payload' in st.session_state:
        payload_data = json.loads(st.session_state['extracted_payload'])
        
        st.markdown("---")
        st.markdown("#### 📋 Web-Agent Injection Payload")
        st.caption("Click the copy button in the top-right of this box, then launch your Bookmarklet on the booking site:")
        injection_string = json.dumps(payload_data)
        st.code(injection_string, language="json")

# --- COLUMN 2: VERIFICATION TERMINAL AND PORTAL LINKS ---
with col2:
    st.subheader("⚙️ Agentic Verification Terminal")
    
    if generate_btn and user_prompt:
        with st.spinner("Gemini is assembling master registry data..."):
            try:
                today_str = datetime.date.today().strftime("%Y-%m-%d")
                
                prompt_context = f"""
                Today's absolute baseline date is: {today_str}.
                Extract booking details and parse the passenger matrix completely using these strict field validation rules:
                
                GENDER MAPPING RULE:
                - Identify passenger gender. Map it exactly to 'Male', 'Female', or 'Transgender' inside the JSON structure.
                
                DOCUMENT PAIRING LOGIC:
                - For 12-digit numeric configurations or explicit Aadhaar mentions:
                  * identity_proof_type = "Aadhaar Card"
                  * photo_identity_type = "Aadhaar Card"
                  * identity_number = [12-digit numeric string]
                - For alphanumeric configurations or explicit Passport mentions:
                  * identity_proof_type = "Passport"
                  * photo_identity_type = "Passport"
                  * identity_number = [Alphanumeric identity string]
                
                ADDRESS & CONTACT FIELDS:
                - Cleanly extract the Name, Age, Mobile No, City, State, Country, and Pincode for every passenger listed.
                - Default 'country' to 'India' if not explicitly stated.
                
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
                st.rerun() # Refresh to instantly move down to the copy window in Column 1
            except Exception as e:
                st.error(f"Gemini Processing Error: {e}")

    if 'extracted_payload' in st.session_state:
        payload_data = json.loads(st.session_state['extracted_payload'])
        
        st.success("✅ Comprehensive Passenger Records Successfully Structured!")
        st.json(payload_data)
        
        st.markdown("### 🧭 Portal Quick Navigation")
        
        if payload_data['booking_type'] == "IRCTC Train":
            target_url = "https://irctc.co.in"
            st.info(f"🚄 **AI Recommendation:** Target Route: **{payload_data['source_city']} ➔ {payload_data['destination_city']}** scheduled for **{payload_data['travel_date']}**")
        else:
            # Updated to point directly to the accurate sub-routed TTD platform dashboard url
            target_url = "https://ttdevasthanams.ap.gov.in/home/dashboard"
            st.info(f"🛕 **AI Recommendation:** Headed to Official TTD Dashboard for slots scheduled for **{payload_data['travel_date']}**")
            
        st.link_button(f"🔗 Open Official {payload_data['booking_type']} Website", target_url, type="primary")
