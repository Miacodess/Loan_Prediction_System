from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import pandas as pd
import sqlite3 
import os # <-- NEW: This helps us find the exact folder path

# --- NEW: FORCE THE DATABASE LOCATION ---
# This finds the exact folder where this python file is saved
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# This tells Python to put the database exactly in that same folder
DB_PATH = os.path.join(BASE_DIR, "loan_records.db")

# 1. Initialize the app
app = FastAPI(title="Bank Loan Prediction Engine")

# 2. Database Setup Function
def setup_database():
    conn = sqlite3.connect(DB_PATH) # <-- Uses the locked path
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS applications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            Gender INTEGER, Married INTEGER, Dependents INTEGER,
            Education INTEGER, Self_Employed INTEGER, ApplicantIncome REAL,
            CoapplicantIncome REAL, LoanAmount REAL, Loan_Amount_Term REAL,
            Credit_History REAL, Property_Area INTEGER, Prediction TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Run the setup right away
setup_database()

# 3. Load the saved brain (.joblib)
try:
    # Ensure it looks for the model folder in the same base directory
    MODEL_PATH = os.path.join(BASE_DIR, "model", "loan_model.joblib")
    model = joblib.load(MODEL_PATH)
    print("✅ Model loaded successfully into the engine!")
except Exception as e:
    print(f"🚨 Error loading model: {e}")

# 4. The Blueprint
class LoanApplication(BaseModel):
    Gender: int; Married: int; Dependents: int; Education: int; Self_Employed: int
    ApplicantIncome: float; CoapplicantIncome: float; LoanAmount: float
    Loan_Amount_Term: float; Credit_History: float; Property_Area: int      

# 5. The Listener Endpoint
@app.post("/predict")
def predict_loan(application: LoanApplication):
    # Convert data for the model
    input_data = pd.DataFrame([application.model_dump()])
    
    # Get the prediction
    prediction = model.predict(input_data)
    result = "Approved" if prediction[0] == 1 else "Denied"
    
    # --- SAVE TO DATABASE ---
    conn = sqlite3.connect(DB_PATH) # <-- Uses the locked path
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO applications (
            Gender, Married, Dependents, Education, Self_Employed, 
            ApplicantIncome, CoapplicantIncome, LoanAmount, Loan_Amount_Term, 
            Credit_History, Property_Area, Prediction
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        application.Gender, application.Married, application.Dependents, 
        application.Education, application.Self_Employed, application.ApplicantIncome, 
        application.CoapplicantIncome, application.LoanAmount, application.Loan_Amount_Term, 
        application.Credit_History, application.Property_Area, result
    ))
    conn.commit()
    conn.close()
    
    return {"prediction": result, "status_code": 200}

@app.get("/")
def read_root():
    return {"message": f"Engine is online! Database saved at: {DB_PATH}"}