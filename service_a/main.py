# service_a.py
from fastapi import FastAPI
app = FastAPI()

@app.get("/service-a")
def hello_a():
    return {"service": "A", "message": "Hello from Service A"}

@app.get("/")
def root():
    return {"message": "Service A is running"}
