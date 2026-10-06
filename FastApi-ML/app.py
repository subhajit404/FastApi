from fastapi import FastAPI
from pydantic import BaseModel, Field, computed_field
from fastapi.responses import JSONResponse
from typing import Literal, Annotated
import pickle
import pandas as pd


# Load trained ML model
with open("model.pkl", "rb") as file:
    model = pickle.load(file)


# City categories
tier_1_cities = [
    "Mumbai",
    "Delhi",
    "Bangalore",
    "Chennai",
    "Kolkata",
    "Hyderabad",
    "Pune"
]

tier_2_cities = [
    "Jaipur",
    "Chandigarh",
    "Indore",
    "Lucknow",
    "Patna",
    "Ranchi",
    "Visakhapatnam",
    "Coimbatore",
    "Bhopal",
    "Nagpur",
    "Vadodara",
    "Surat",
    "Rajkot",
    "Jodhpur",
    "Raipur",
    "Amritsar",
    "Varanasi",
    "Agra",
    "Dehradun",
    "Mysore",
    "Jabalpur",
    "Guwahati",
    "Thiruvananthapuram",
    "Ludhiana",
    "Nashik",
    "Allahabad",
    "Udaipur",
    "Aurangabad",
    "Hubli",
    "Belgaum",
    "Salem",
    "Vijayawada",
    "Tiruchirappalli",
    "Bhavnagar",
    "Gwalior",
    "Dhanbad",
    "Bareilly",
    "Aligarh",
    "Gaya",
    "Kozhikode",
    "Warangal",
    "Kolhapur",
    "Bilaspur",
    "Jalandhar",
    "Noida",
    "Guntur",
    "Asansol",
    "Siliguri"
]


# Create FastAPI application
app = FastAPI()


# Pydantic model to validate input data
class UserInput(BaseModel):

    age: Annotated[
        int,
        Field(
            ...,
            gt=0,
            lt=120,
            description="Age of the user"
        )
    ]

    weight: Annotated[
        float,
        Field(
            ...,
            gt=0,
            description="Weight of the user in kg"
        )
    ]

    height: Annotated[
        float,
        Field(
            ...,
            gt=0,
            lt=2.5,
            description="Height of the user in meters"
        )
    ]

    income_lpa: Annotated[
        float,
        Field(
            ...,
            gt=0,
            description="User annual income in LPA"
        )
    ]

    smoker: Annotated[
        bool,
        Field(
            ...,
            description="Whether the user is a smoker"
        )
    ]

    city: Annotated[
        str,
        Field(
            ...,
            description="User city"
        )
    ]

    occupation: Annotated[
        Literal[
            "retired",
            "freelancer",
            "student",
            "government_job",
            "business_owner",
            "unemployed",
            "private_job"
        ],
        Field(
            ...,
            description="User occupation"
        )
    ]


    # Calculate BMI
    @computed_field
    @property
    def bmi(self) -> float:
        return self.weight / (self.height ** 2)


    # Calculate lifestyle risk
    @computed_field
    @property
    def lifestyle_risk(self) -> str:

        if self.smoker and self.bmi > 30:
            return "high"

        elif self.smoker or self.bmi > 27:
            return "medium"

        else:
            return "low"


    # Determine city tier
    @computed_field
    @property
    def city_tier(self) -> int:

        if self.city in tier_1_cities:
            return 1

        elif self.city in tier_2_cities:
            return 2

        else:
            return 3


    # Determine age group
    @computed_field
    @property
    def age_group(self) -> str:

        if self.age < 25:
            return "young"

        elif self.age < 45:
            return "adult"

        elif self.age < 60:
            return "middle_aged"

        else:
            return "senior"


# Prediction endpoint
@app.post("/predict")
def predict_premium(data: UserInput):

    # Create dataframe for model prediction
    input_df = pd.DataFrame([{
        "bmi": data.bmi,
        "age_group": data.age_group,
        "lifestyle_risk": data.lifestyle_risk,
        "city_tier": data.city_tier,
        "income_lpa": data.income_lpa,
        "occupation": data.occupation
    }])

    # Make prediction
    prediction = model.predict(input_df)[0]

    # Return prediction
    return JSONResponse(
        status_code=200,
        content={
            "predicted_category": prediction
        }
    )