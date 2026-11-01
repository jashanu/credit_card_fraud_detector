from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import joblib
import pandas as pd

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

model = joblib.load('fraud_model.pkl')
model_columns = joblib.load('model_columns.pkl')

class Transaction(BaseModel):
    amt: float
    category: str
    hour: int
    age: int
    city_pop: int

@app.post("/predict")
def predict(transaction: Transaction):
    input_df = pd.DataFrame([transaction.dict()])
    input_df = pd.get_dummies(input_df, columns=['category'])
    input_df = input_df.reindex(columns=model_columns, fill_value=0)
    
    prediction = model.predict(input_df)[0]
    probability = model.predict_proba(input_df)[0][1]
    
    return {
        "is_fraud": bool(prediction),
        "fraud_probability": round(float(probability), 4)
    }