from pydantic import BaseModel,EmailStr, AnyUrl,Field
from typing import List, Dict,Optional, Annotated


class Patient(BaseModel):
    name : str = Field(max_length=50)
    age : int = Field(gt=0, le=80)
    email : EmailStr
    Linkedin : AnyUrl
    weight : float =Field(gt=0)
    marred : Optional[bool] = None
    allergy : Optional[List[str]] = Field(default=None,max_length=5) 
    Phone : int 

def insert_paitent_details(patient:Patient):
    print(patient.name)
    print(patient.age)
    print(patient.allergy)
    print("Inserted")

paitent_info = {'name':"Subhajit", 'age':30, 'email':'Abc@gmail.com', 'Linkedin':"https://www.linkedin.com/in/subhajit-patra101/?isSelfProfile=true",'weight':68.5,'marred':False, 'allergy':['flower','Dust','water'], 'Phone':7418529630} 

Patient1 = Patient(**paitent_info)

insert_paitent_details(Patient1)