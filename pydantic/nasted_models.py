from pydantic import BaseModel

class Address(BaseModel):
    city :str
    state : str
    pin : int
    
class Patient(BaseModel):
    name : str
    gender : str
    age : int 
    address : Address


address_dict = {'city':'Delhi','state':'Delhi','pin':721193}
address1 = Address(**address_dict)

patient_dict = {'name':'Subhajit', 'gender':"M",'age':21,'address':address1}

Patient1 = Patient(**patient_dict)

print(Patient1)
