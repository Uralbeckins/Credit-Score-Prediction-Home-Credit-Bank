import os
import streamlit as st
import requests
from datetime import datetime, timedelta

st.markdown(
    """
    <style>
    html, body, [class*="css"]  {
        font-size: 22px;
    }
    </style>
    """,
    unsafe_allow_html=True
)


api_url = os.getenv("BACKEND_URL", "http://backend:8000")





st.set_page_config(page_title="💶 Home Credit Scoring Demo", layout="wide")
st.title("🏦 Credit Scoring Interactive Demo")

st.badge("FastAPI", color="green")
st.badge("Streamlit", color="red")
st.badge("Machine Learning", color="blue")
st.markdown("Fill in the form below to get your credit score prediction 📊")

# --- FIRST ROW (Personal Info + Education) ---
col_left, col_right = st.columns(2)

with col_left:
    st.header("👤 Personal Information")
    sex = st.segmented_control("Gender", ["Male ", "Female"], selection_mode='single')
    age = st.number_input("Age (years)", min_value=18, max_value=100, value=18, step=1)
    marital_status = st.selectbox(
        "Marital Status", 
        ["Single", "Married", "Civil marriage", "Widow/Widower", "Separated"]
    )
    children = st.number_input("Number of Children 👶", min_value=0, max_value=10, value=1)

with col_right:
    st.header("🎓 Education & Work")
    education = st.selectbox(
        "Education Level", 
        ["Secondary", "Higher", "Incomplete higher", "Academic degree"]
    )
    income_type = st.selectbox(
        "Income Type", 
        ["Working", "Commercial associate", "Pensioner", "State servant", "Unemployed"]
    )
    years_employed = st.slider("Years Employed", min_value=0, max_value=50, value=1, step=1)
    registration_date = st.date_input("Registration Date", value=datetime.today() - timedelta(days=365*5))
    id_publish_date = st.date_input("ID Publish Date", value=datetime.today() - timedelta(days=365*10))

# --- Separator line between first and second row ---
st.markdown("---")

# --- SECOND ROW (Housing + Financial) ---
col_left, col_right = st.columns(2)

with col_left:
    st.header("🏠 Housing & Property")
    own_car = st.radio("Own a Car?", ["Yes 🚗", "No 🚶‍♂️"], horizontal=True)
    own_realty = st.radio("Own Realty?", ["Yes 🏡", "No 🏕️"], horizontal=True)
    housing_type = st.selectbox(
        "Housing Type", 
        ["House / Apartment", "With parents", "Municipal apartment", "Rented apartment", "Office apartment"]
    )

with col_right:
    st.header("💰 Financial Information")
    col1, col2 = st.columns(2)
    with col1:
        income = st.number_input("Monthly Income", min_value=0, value=50000, step=1000, format="%d")
    with col2:
        credit_amount = st.number_input("Credit Amount", min_value=0, value=300000, step=5000, format="%d")
    annuity = st.number_input("Monthly Annuity Payment", min_value=0, value=15000, step=500, format="%d")

# --- ADDITIONAL INFO in a card ---
st.markdown("---")
st.markdown("<h2 style='text-align: center;'>📌 Additional Information</h2>", unsafe_allow_html=True)

emergency_state = st.segmented_control("Emergency State of Region", ["Unknown", "No", "Yes"], selection_mode='single')
docs_provided = st.multiselect(
    "Documents Provided", 
    ["Passport", "Income statement", "Employment contract", "Credit history", "Other"]
)




if st.button("Predict"):
    payload = {"AMT_INCOME_TOTAL": float(income), "AMT_CREDIT": float(credit_amount)}
    try:
        r = requests.post(f"{api_url}/predict", json=payload, timeout=10)
        r.raise_for_status()
        # st.write("Score:", round(float(r.json().get("score")), 3))
        for_print = round(float(r.json().get("score")), 3)
        st.subheader(f"Score: {for_print}")
    except Exception as e:
        st.error(f"Request failed: {e}")