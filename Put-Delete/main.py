from fastapi import FastAPI,HTTPException,Path,Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel,Field,computed_field
from typing import Annotated,Literal,Optional
import json

app =FastAPI()

class Patient(BaseModel):
    
    id : Annotated[str, Field(...,description="Id of the Patient ", examples=['P001'])]
    name : Annotated[str, Field(...,description="Enter the PAtient Name")]
    city : Annotated[str,Field(...,description="Enter the city")]
    age : Annotated[int, Field(...,gt=0,lt=120, description="Enter the age")]
    gender : Annotated[
    Literal['Male','Femal','Other'],
    Field(...,description="Enter the Geneder")
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


class Patient_Update(BaseModel):
    name: Annotated[Optional[str], Field(default=None)]
    city: Annotated[Optional[str], Field(default=None)]
    age: Annotated[Optional[int], Field(default=None, gt=0)]
    gender: Annotated[Optional[Literal['male', 'female']], Field(default=None)]
    height: Annotated[Optional[float], Field(default=None, gt=0)]
    weight: Annotated[Optional[float], Field(default=None, gt=0)]
    
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


@app.put('/edit/{patient_id}')
def update_patient(patient_id:str,patient_update:Patient_Update):
    data = load_data()
    
    if patient_id not in data:
        raise HTTPException(status_code=404, detail="Patient id not found")
    
    existing_patient_info = data[patient_id]
    
    updated_patient_info = patient_update.model_dump(exclude_unset=True)
    
    for key,value in updated_patient_info.items():
         existing_patient_info[key] = value
         
    
    existing_patient_info['id'] = patient_id
    patient_pydantic_obj = Patient(**existing_patient_info)
    
    existing_patient_info = patient_pydantic_obj.model_dump(exclude='id')
     
    data[patient_id] = existing_patient_info
      
    save_data(data)
    
    return JSONResponse(status_code=200,content="Patient Updated")
    