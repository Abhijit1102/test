from fastapi import FastAPI
from faker import Faker
import random

app = FastAPI()
fake = Faker()

@app.get("/")
def home():
    return {"message": "Random User API"}

@app.get("/user")
def get_random_user():
    return {
        "name": fake.name(),
        "email": fake.email(),
        "phone": fake.phone_number(),
        "address": fake.address(),
        "company": fake.company(),
    }


