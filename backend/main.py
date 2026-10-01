from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import json
import os
import uuid

# Base directory for reliable file paths regardless of where the server is launched
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "data.json")

app = FastAPI(
    title="Cyber Physical Healthcare System",
    description="Backend for the healthcare mobile application",
    version="1.0"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Patient data structure
class Patient(BaseModel):
    age: int
    weight: float
    bmi: Optional[float] = None
    gender: str
    known_disease: Optional[str] = None
    allergies: Optional[str] = None
    emergency_type: str


# Read data.json
def load_data():
    if not os.path.exists(DATA_FILE):
        return {"patients": []}

    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)
            if not isinstance(data, dict) or "patients" not in data:
                return {"patients": []}
            return data
    except Exception:
        return {"patients": []}


# Write to data.json
def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)


# Test endpoint
@app.get("/")
def home():
    return {
        "message": "Cyber Physical Healthcare Backend is running!"
    }


# Add a patient
@app.post("/patients")
def create_patient(patient: Patient):
    data = load_data()

    patient_id = "P" + str(uuid.uuid4())[:8]

    patient_data = {
        "patient_id": patient_id,
        "age": patient.age,
        "weight": patient.weight,
        "bmi": patient.bmi,
        "gender": patient.gender,
        "known_disease": patient.known_disease,
        "allergies": patient.allergies,
        "emergency_type": patient.emergency_type
    }

    data["patients"].append(patient_data)
    save_data(data)

    return {
        "message": "Patient data saved successfully",
        "patient": patient_data
    }


# Get all patients
@app.get("/patients")
def get_patients():
    data = load_data()
    return data


# Get patient by ID
@app.get("/patients/{patient_id}")
def get_patient(patient_id: str):
    data = load_data()

    for patient in data["patients"]:
        if patient.get("patient_id") == patient_id:
            return patient

    raise HTTPException(
        status_code=404,
        detail="Patient not found"
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True, app_dir=BASE_DIR)