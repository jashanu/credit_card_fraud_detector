# Credit Card Fraud Detector

A full stack machine learning app that flags fraudulent credit card transactions in real time. A trained Random Forest model sits behind a FastAPI backend, and a React frontend lets you enter a transaction and see the result instantly.

## Results

The model was trained on about 1.3 million transactions, where fraud is very rare. A simple baseline model looked fine on overall accuracy but failed at the real job: only 4 percent of its fraud alerts were correct. After addressing the class imbalance and comparing a simple model against a more advanced one, the final Random Forest reached:

Precision: 86 percent (up from 4 percent)
Recall: 85 percent

In plain terms, about 86 percent of the transactions it flags are really fraud, and it still catches about 85 percent of all fraud.

## How it works

The model uses five inputs about a transaction:

amt: transaction amount
category: merchant category
hour: hour of the day
age: cardholder age
city_pop: population of the cardholder's city

The backend exposes one endpoint, POST /predict. Example request:

```json
{
  "amt": 120.50,
  "category": "grocery_pos",
  "hour": 23,
  "age": 34,
  "city_pop": 50000
}
```

Response shape (values here are illustrative):

```json
{
  "is_fraud": false,
  "fraud_probability": 0.0312
}
```

## Tech stack

Python, pandas, scikit-learn (model training), FastAPI (backend), React with Vite (frontend)

## Project structure

```
main.py              FastAPI backend that serves predictions
explore.ipynb        data exploration, training, and evaluation
model_columns.pkl    column order the model expects
scaler.pkl           saved scaler
frontend/            React app
requirements.txt     Python dependencies
```

## Setup

### 1. Get the data

The dataset is not included because the files are too large for GitHub. Download the [Credit Card Transactions Fraud Detection Dataset](https://www.kaggle.com/datasets/kartik2112/fraud-detection) from Kaggle and place fraudTrain.csv and fraudTest.csv in the project root.

### 2. Build the model

The trained model file (fraud_model.pkl) is about 52 MB, so it is not stored in this repo. Open explore.ipynb and run all cells. This trains the model and saves fraud_model.pkl, scaler.pkl, and model_columns.pkl.

### 3. Run the backend

The app needs two terminals open at the same time. In the first one, create a virtual environment, install the dependencies, and start the server (Windows commands shown; on Mac or Linux, activate with source venv/bin/activate):

```
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```

Wait for the message that Uvicorn is running on http://127.0.0.1:8000, and leave this terminal open.

### 4. Run the frontend

In a second terminal:

```
cd frontend
npm install
npm run dev
```

Open http://localhost:5173, fill in the form, and click Check Transaction. Both terminals must stay running while you use the app. If the page says it could not reach the fraud detection API, the backend has stopped, so start it again with the commands in step 3.

## Notes

The backend only accepts requests from http://localhost:5173, so run the frontend on that port. If loading the model fails with a scikit-learn version error, rebuild it by running the notebook again with your installed version.
