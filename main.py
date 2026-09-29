from fastapi import FastAPI,Path,HTTPException,Query
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
def view_patient(patient_id: str  = Path(...,description="ID of the patient in the database",example="P001") ):
    #load all paitent data
    data = load_data()
    if patient_id in data:
        return data[patient_id]
    raise HTTPException(status_code=404,detail="patient not found ")

@app.get("/sort")
def sort_patients(sort_by:str = Query(...,description="Sort on the bases of height, weight or bmi"),
                  order:str = Query('asc',description="Sort in asc or desc order ")):
    valid_fied = ['height','weight','bmi']
    orders = ['asc','desc']
    if sort_by not in valid_fied:
        raise HTTPException(status_code=400,
                            detail=f"Invalid field, select from {valid_fied}")
        
    if order not in orders:
        raise HTTPException(status_code=400,
                            detail=f"Invalid order, select from {orders}")
        
    data = load_data()
    
    sort_order = True if order == 'desc' else False
    
    sorted_data = sorted(data.values(), key =lambda x: x.get(sort_by,0),reverse = sort_order)
    
    return sorted_data