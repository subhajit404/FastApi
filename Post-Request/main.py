from fastapi import FastAPI,HTTPException,Path,Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel,Field,computed_field
from typing import Annotated,Literal
import json

app =FastAPI()

class Patient(BaseModel):
    
    id : Annotated[str, Field(..., description="Id of the Patient ", examples=['P001'])]
    name : Annotated[str, Field(...,description="Enter the PAtient Name")]
    city : Annotated[str,Field(...,description="Enter the city")]
    age : Annotated[int, Field(..., gt=0,lt=120, description="Enter the age")]
    gender : Annotated[
    Literal['Male','Femal','Other'],
    Field(..., description="Enter the Geneder")
    ]
    height : Annotated[float,Field(...,gt= 0,description="Enter the Height ")]
    weight : Annotated[float, Field(...,gt= 0, description="Enter the weight in kg ")]
    
    
    @computed_field
    @property
    def bmi(self) -> float:
        bmi = round(self.weight / ((self.height / 100) ** 2), 2)
        return bmi


    @computed_field
    @property
    def verdicit(self) -> str:
        if self.bmi <18.5 :
            return 'Under Weight'
        elif self.bmi <25 :
            return 'Normal'
        elif self.bmi < 30:
            return 'OverWeight'
        else :
            return "Obbsie"
        
def load_data():
    with open('patients.json','r') as file:
        data = json.load(file)
    return data
        
def save_data(data):
    with open('patients.json','w') as file:
        json.dump(data,file)
        
@app.post('/create')
def create_patient(patient: Patient):

    # load existing data
    data = load_data()

    # check if the patient already exists
    if patient.id in data:
        raise HTTPException(status_code=400, detail='Patient already exists')

    # new patient add to the database
    data[patient.id] = patient.model_dump(exclude=['id'])
    

    # save into the json file
    save_data(data)

    return JSONResponse(status_code=201, content={'message':'patient created successfully'})


