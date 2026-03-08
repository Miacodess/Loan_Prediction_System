# Aurora Loan Portal

A machine learning web application that predicts bank loan eligibility based on applicant demographics and financial details.

## Project Structure
This project is separated into four main components:
* **Machine Learning Model:** A Logistic Regression model trained on historical banking data to classify loan applications as approved or denied.
* **Backend API (FastAPI):** A REST API that loads the trained `.joblib` model and processes incoming prediction requests.
* **Database (SQLite):** A local database that logs every application's input features and final prediction.
* **Frontend UI (Streamlit):** A web interface that collects user inputs and communicates with the backend via HTTP requests.

## Tech Stack
* **Language:** Python 3
* **Machine Learning:** `scikit-learn`, `pandas`, `joblib`
* **Backend:** `fastapi`, `uvicorn`
* **Frontend:** `streamlit`, `requests`
* **Database:** `sqlite3`

## How to Run Locally

To run this application, you need to start both the backend server and the frontend UI in separate terminal windows.

### 1. Install Dependencies
```bash
pip install -r requirements.txt