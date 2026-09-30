from pydantic import BaseModel,EmailStr, AnyUrl,Field,field_validator
from typing import List, Dict,Optional, Annotated


class Patient(BaseModel):
    name : Annotated[str, Field(max_length=50,title="Enter the Patient name ",description='Enter Length Between 1 to 50',examples=["Subhajit", "Amit"])]
    age : int = Field(gt=0, le=80)
    email : EmailStr
    Linkedin : AnyUrl
    weight : float =Field(gt=0)
    marred : Optional[bool] = None
    allergy : Optional[List[str]] = Field(default=None,max_length=5) 
    Phone : int 
    
    @field_validator('email')
    @classmethod
    def email_validate(cls,value):
        valid_domains = ['hdfc.com','icici.com']

        domain_name = value.split('@')[-1]
        if domain_name not in valid_domains:
            raise ValueError("This is is not an valid Domain")
        
        return value

def insert_paitent_details(patient:Patient):
    print(patient.name)
    print(patient.age)
    print(patient.allergy)
    print("Inserted")

paitent_info = {'name':"Subhajit", 'age':30, 'email':'Abc@hdfc.com', 'Linkedin':"https://www.linkedin.com/in/subhajit-patra101/?isSelfProfile=true",'weight':68.5,'marred':False, 'allergy':['flower','Dust','water'], 'Phone':7418529630} 

Patient1 = Patient(**paitent_info)

insert_paitent_details(Patient1)