from fastapi import FastAPI,Path
import json



app = FastAPI()

def load_data():
    with open('patients.json','r') as file:
        data = json.load(file)
    
    return data

@app.get("/")
def hello():
    return {"Message":"Patients Mannagement System API"}


@app.get("/about")
def about():
    return {"message":"A fully functional api manage your patien records "}

@app.get('/view')
def view():
    data = load_data()
    return data

@app.get("/patient/{patient_id}")
def view_patient(patient_id: str  = Path(...,description="ID of the paitent in the database",example="P001") ):
    #load all paitent data
    data = load_data()
    if patient_id in data:
        return data[patient_id]
    return {'error':"patient not found"}
    