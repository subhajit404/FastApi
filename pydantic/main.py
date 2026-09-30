from pydantic import BaseModel,EmailStr
from typing import List, Dict,Optional


class Patient(BaseModel):
    name : str
    age : int 
    email : EmailStr
    weight : float
    marred : Optional[bool] = None
    allergy : Optional[List[str]] = None
    Phone : int 

def insert_paitent_details(patient:Patient):
    print(patient.name)
    print(patient.age)
    print(patient.allergy)
    print("Inserted")

paitent_info = {'name':"Subhajit", 'age':30, 'email':'Abc@gmail.com','weight':68.5,'marred':False, 'allergy':['flower','Dust','water'], 'Phone':7418529630} 

Patient1 = Patient(**paitent_info)

insert_paitent_details(Patient1)