# 🌐 Cloud-Native Agentic AI Travel Controller

A 100% web-native Agentic AI application that bridges natural conversational language with rigid transactional travel booking portals (**IRCTC** and **TTD**). 

This platform uses **Google Gemini 2.5 Flash** as the analytical brain to decompose unstructured chat data into validated KYC profile matrices and connects to a client-side **Browser Bookmarklet** macro to bypass server anti-bot rules safely.

---

## 📂 Repository File Structure
Your GitHub repository must contain only these two files to deploy perfectly on Streamlit Cloud:
* `app.py` - The core frontend interface and Gemini data parsing engine.
* `requirements.txt` - Installs cloud packages (`streamlit`, `google-genai`, `pydantic`).

---

## 🛠️ Step 1: Create Your Web Browser Agent (Bookmarklet)
Because cloud servers cannot manipulate your personal computer screen directly due to security sandboxes, you use a lightweight JavaScript macro to act as the agent's hands.

1. Open your desktop web browser (Chrome, Edge, or Brave).
2. Open your **Bookmark Manager** (press `Ctrl + D` or `Cmd + D`).
3. Click "More" or add a new bookmark manually. Name it exactly: **`🤖 Run Travel Agent`**
4. Clear out the web link URL field completely and paste this exact single-line automation script inside it:

```javascript
javascript:(async function(){const text=await navigator.clipboard.readText();try{const data=JSON.parse(text);if(location.href.includes("irctc.co.in")){alert("🚄 Agent Active: Filling IRCTC Route...");if(data.source_city){document.querySelector("p-autocomplete[id='origin'] input").value=data.source_city;}if(data.destination_city){document.querySelector("p-autocomplete[id='destination'] input").value=data.destination_city;}if(data.travel_date){document.querySelector("p-calendar[id='jDate'] input").value=data.travel_date;}}else if(location.href.includes("ttdevasthanams.ap.gov.in")){alert("🛕 Agent Active: Injecting Master Profile Matrix onto TTD Form...");data.passengers.forEach((p,i)=>{try{const rows=document.querySelectorAll(".pilgrim-row, .passenger-details-form, tr");if(rows[i]){const nameIn=rows[i].querySelector("input[placeholder*='Name'], input[name*='name']");if(nameIn)nameIn.value=p.name;const ageIn=rows[i].querySelector("input[placeholder*='Age'], input[name*='age']");if(ageIn)ageIn.value=p.age;const genSel=rows[i].querySelector("select[name*='gender'], select");if(genSel){if(p.gender==='Transgender')genSel.value='T';else genSel.value=p.gender==='Male'?'M':'F';}const idTypeSel=rows[i].querySelector("select[id*='idProof'], select[id*='Identity'], select[name*='proof']");if(idTypeSel){idTypeSel.value=p.identity_proof_type;}const photoTypeSel=rows[i].querySelector("select[id*='photoProof'], select[id*='Photo']");if(photoTypeSel){photoTypeSel.value=p.photo_identity_type;}const idNumIn=rows[i].querySelector("input[placeholder*='Number'], input[id*='Number'], input[name*='idNo']");if(idNumIn)idNumIn.value=p.identity_number;const mobIn=rows[i].querySelector("input[placeholder*='Mobile'], input[name*='mobile'], input[type='tel']");if(mobIn)mobIn.value=p.mobile_no;const cityIn=rows[i].querySelector("input[placeholder*='City'], input[name*='city']");if(cityIn)cityIn.value=p.city;const stateIn=rows[i].querySelector("input[placeholder*='State'], input[name*='state']");if(stateIn)stateIn.value=p.state;const pinIn=rows[i].querySelector("input[placeholder*='Pin'], input[name*='pin'], input[name*='zip']");if(pinIn)pinIn.value=p.pincode;}}catch(err){console.log('Row input drop:',err);});alert('✅ Completed! All structural records, inclusive gender settings, identities, full addresses, and contact fields populated.');}else{alert('🤖 System Ready. Please load your booking table form page first.');}}catch(e){alert('❌ Error: Invalid structure. Copy the newest block from your Streamlit workspace first!');}})();
```

---

## 🏁 Step 2: The End-to-End Operational Lifecycle

Once your application is deployed on **share.streamlit.io**, follow these seamless execution steps:

1. **Authenticate:** Paste your personal Gemini API Key into the secure password text input field in the sidebar.
2. **Conversational Prompt:** Type a comprehensive booking requirement in the text area block. 
3. **Decompose Matrix:** Tap **`🚀 Process via Agent Brain`**. The model immediately references the dynamic system server date clock, validates structural fields, and drops a clean compilation string into the **`📋 Web-Agent Injection Payload`** code section directly underneath your button.
4. **Copy Output:** Click the native web **Copy** icon located in the upper right-hand corner of the generated JSON code box.
5. **Portal Navigation:** Click the primary blue **`🔗 Open Official Website`** button on the right to navigate straight to the live IRCTC engine or the secure **Official TTD Dashboard** (`https://ap.gov.in`).
6. **Execute Agent:** Log in through the captcha/OTP security walls manually. Once you arrive at the passenger fields entry page, simply tap your **`🤖 Run Travel Agent`** favorite bookmarklet. The macro reads the clipboard variables and types out your multi-passenger matrix forms in a fraction of a second.

---

### 🧪 Sample Dynamic Test Queries

* **TTD Seva Test:** 
  > *“Book TTD slots for tomorrow. Passenger is Kiran Sharma, 31, Male, Aadhaar: 111122223333, Mobile: 9898989898, resident of New Delhi, state of Delhi, Pincode 110001.”*
  
* **IRCTC Train Test:**
  > *“Need a train booking from NDLS to TPTY for today. Passenger is Sarah Jenkins, age 29, Female, Passport identity number K87654321, Phone 9123456789, living in Mumbai, Maharashtra, Pin 400001.”*
