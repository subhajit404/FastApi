from fastapi import FastAPI
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