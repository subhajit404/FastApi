from pydantic import BaseModel

class Patient(BaseModel):
    name : str
    age : int 
    # weight : float

def insert_paitent_details(patient:Patient):
    print(patient.name)
    print(patient.age)
    print("Inserted")

paitent_info = {'name':"Subhajit",'age':"30"}

Patient1 = Patient(**paitent_info)

insert_paitent_details(Patient1)