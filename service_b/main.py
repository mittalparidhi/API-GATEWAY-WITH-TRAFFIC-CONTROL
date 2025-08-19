# service_a.py
from fastapi import FastAPI
app = FastAPI()

@app.get("/service-b")
def hello_a():
    return {"service": "B", "message": "Hello from Service B"}

@app.get("/")
def root():
    return {"message": "Service B is running"}

