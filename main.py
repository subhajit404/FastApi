from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def hello():
    return {"Message":"Hello"}


@app.get("/about")
def about():
    return {"message":"Who are you"}