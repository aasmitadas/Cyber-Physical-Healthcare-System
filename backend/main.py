from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import json
import os
import uuid

app = FastAPI(
    title="Cyber Physical Healthcare System",
    description="Backend for the healthcare mobile application",
    version="1.0"
)

DATA_FILE = "data.json"

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

    with open(DATA_FILE, "r") as file:
        return json.load(file)


# Write to data.json

def save_data(data):
    with open(DATA_FILE, "w") as file:
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

@app.get("/patients/{patient_id}")
def get_patient(patient_id: str):

    data = load_data()

    for patient in data["patients"]:

        if patient["patient_id"] == patient_id:
            return patient

    raise HTTPException(
        status_code=404,
        detail="Patient not found"
    )