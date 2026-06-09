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

# Generate multiple users
@app.get("/users/{count}")
def get_multiple_users(count: int):
    return {
        "users": [
            {
                "name": fake.name(),
                "email": fake.email(),
                "company": fake.company(),
            }
            for _ in range(count)
        ]
    }

