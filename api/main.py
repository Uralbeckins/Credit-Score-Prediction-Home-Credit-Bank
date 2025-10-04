from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import pandas as pd
import os

app = FastAPI()

MODEL_PATH = os.getenv("MODEL_PATH", "models/pipeline_logreg.joblib")
model = joblib.load(MODEL_PATH)

class Features(BaseModel):
    AMT_INCOME_TOTAL: float
    AMT_CREDIT: float

@app.get("/health")
def health():
    return {"status":"ok"}

@app.post("/predict")
def predict(payload: Features):
    row = pd.DataFrame([payload.dict()])
    proba = float(model.predict_proba(row)[:,1][0])
    return {"score": proba}


# cd "/Users/uralgimazov/Desktop/Python/Home Credit"
# docker compose -f docker/docker-compose.yml up --build
# open http://localhost:8501

# cd "/Users/uralgimazov/Desktop/Python/Home Credit"
# docker compose -f docker/docker-compose.yml


# cd "/Users/uralgimazov/Desktop/Python/Home Credit"
# docker compose -f docker/docker-compose.yml ps
# curl -I http://127.0.0.1:8501 || echo "no ui"
# open http://localhost:8501