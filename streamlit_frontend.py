import streamlit as st
import requests

# --- 1. PAGE CONFIGURATION & TAB STYLING ---
st.set_page_config(page_title="Aurora Loan Portal", page_icon="🇳🇬", layout="centered")

# --- 2. CUSTOM CSS (PERMANENT DARK MODE & FIXED ALERTS) ---
st.markdown("""
    <style>
    /* Clean light gray background for the main app */
    .stApp { background-color: #F4F6F6; }
    
    /* Headers and regular text */
    h1, h2, h3 { color: #008751 !important; font-family: 'Helvetica Neue', sans-serif; }
    p { color: #333333; } /* Forces normal text to be dark and readable */
    
    /* The Main Predict Button */
    div.stButton > button:first-child {
        background-color: #008751; color: #FFFFFF; border: none;
        border-radius: 8px; padding: 10px 24px; font-size: 18px;
        font-weight: bold; width: 100%; transition: 0.3s;
    }
    div.stButton > button:first-child:hover {
        background-color: #005c37; color: #FFFFFF; border: 1px solid #005c37;
    }
    
    /* Input Labels */
    .stSelectbox label, .stNumberInput label { font-weight: bold; color: #333333 !important; }

    /* --- THE INPUT CELLS (PERMANENT DARK MODE) --- */
    div[data-baseweb="select"] > div, 
    div[data-baseweb="input"] > div {
        background-color: #2b2b2b !important; /* Sleek Dark Grey */
        border: 1px solid #555555 !important;
        border-radius: 6px;
        transition: all 0.3s ease-in-out;
    }
    
    /* Force all text inside the boxes to be Bright White */
    div[data-baseweb="select"] *, 
    div[data-baseweb="input"] *,
    div[data-baseweb="select"] input,
    div[data-baseweb="input"] input {
        color: #FFFFFF !important;
        -webkit-text-fill-color: #FFFFFF !important;
    }
    
    /* Hover State: Subtle Green Border */
    div[data-baseweb="select"] > div:hover, 
    div[data-baseweb="input"] > div:hover {
        border: 1px solid #008751 !important; 
    }

    /* Active State (Typing) */
    div[data-baseweb="select"] > div:focus-within, 
    div[data-baseweb="input"] > div:focus-within {
        background-color: #1a1a1a !important; /* Jet Black */
        border: 2px solid #008751 !important; 
    }

    /* --- THE ALERT BOXES FIX (Warnings, Success, Errors) --- */
    div[data-testid="stAlert"] {
        background-color: #FFFFFF !important; /* Clean white background */
        border: 1px solid #CCCCCC !important; /* Subtle border */
        border-left: 5px solid #008751 !important; /* Nigerian Green accent stripe */
        box-shadow: 0px 4px 6px rgba(0,0,0,0.1) !important; /* Slight 3D drop shadow */
    }
    
    /* Force the text inside the alerts to be jet black */
    div[data-testid="stAlert"] * {
        color: #000000 !important;
        font-weight: 500 !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- 3. THE USER INTERFACE ---
st.title("🇳🇬 Aurora Loan Portal")
st.markdown("### Professional Eligibility Assessment System")
st.write("Please enter the applicant's details below. Our AI engine will process the data instantly.")
st.markdown("---")

# Clean 2-column layout (Empty by default, NO placeholders)
col1, col2 = st.columns(2)

with col1:
    gender = st.selectbox("Gender", ["Male", "Female"], index=None)
    married = st.selectbox("Married", ["Yes", "No"], index=None)
    dependents = st.selectbox("Dependents", ["0", "1", "2", "3+"], index=None)
    education = st.selectbox("Education", ["Graduate", "Not Graduate"], index=None)
    self_employed = st.selectbox("Self Employed", ["Yes", "No"], index=None)
    credit_history = st.selectbox("Credit History", ["Good (1.0)", "Bad (0.0)"], index=None)

with col2:
    applicant_income = st.number_input("Applicant Income (₦)", value=None, step=500.0)
    coapplicant_income = st.number_input("Co-Applicant Income (₦)", value=None, step=500.0)
    loan_amount = st.number_input("Loan Amount (Thousands)", value=None, step=10.0)
    loan_amount_term = st.number_input("Loan Term (Months)", value=None, step=12.0)
    property_area = st.selectbox("Property Area", ["Urban", "Semiurban", "Rural"], index=None)

st.markdown("---")

# --- 4. THE INVISIBLE TRANSLATOR ---
mapping = {
    "Gender": {"Female": 0, "Male": 1},
    "Married": {"No": 0, "Yes": 1},
    "Dependents": {"0": 0, "1": 1, "2": 2, "3+": 3},
    "Education": {"Not Graduate": 0, "Graduate": 1},
    "Self_Employed": {"No": 0, "Yes": 1},
    "Property_Area": {"Rural": 0, "Semiurban": 1, "Urban": 2},
    "Credit_History": {"Bad (0.0)": 0.0, "Good (1.0)": 1.0}
}

# --- 5. SENDING THE DATA TO FASTAPI ---
if st.button("Predict Loan Status"):
    
    # Gather inputs for the bouncer check
    all_user_inputs = [gender, married, dependents, education, self_employed, 
                       applicant_income, coapplicant_income, loan_amount, 
                       loan_amount_term, credit_history, property_area]
    
    if None in all_user_inputs:
        st.warning("⚠️ Please fill out all fields before clicking Predict.")
    else:
        payload = {
            "Gender": mapping["Gender"][gender],
            "Married": mapping["Married"][married],
            "Dependents": mapping["Dependents"][dependents],
            "Education": mapping["Education"][education],
            "Self_Employed": mapping["Self_Employed"][self_employed],
            "ApplicantIncome": applicant_income,
            "CoapplicantIncome": coapplicant_income,
            "LoanAmount": loan_amount,
            "Loan_Amount_Term": loan_amount_term,
            "Credit_History": mapping["Credit_History"][credit_history],
            "Property_Area": mapping["Property_Area"][property_area]
        }

        try:
            with st.spinner('Analyzing applicant data...'):
                response = requests.post("http://127.0.0.1:8000/predict", json=payload)
                
            if response.status_code == 200:
                result = response.json()["prediction"]
                if result == "Approved":
                    st.success(f"✅ STATUS: {result.upper()} - The applicant meets all criteria.")
                    st.balloons() 
                else:
                    st.error(f"❌ STATUS: {result.upper()} - The applicant does not meet the criteria at this time.")
        except requests.exceptions.ConnectionError:
            st.warning("⚠️ Could not connect to the Engine. Please ensure FastAPI is running.")