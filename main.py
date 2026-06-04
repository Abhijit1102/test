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
        "job": fake.job(),
    }


@app.get("/company")
def get_random_company():
    return {
        "company": fake.company(),
        "industry": fake.bs(),
        "website": fake.url(),
        "address": fake.address(),
    }


@app.get("/location")
def get_random_location():
    return {
        "city": fake.city(),
        "state": fake.state(),
        "country": fake.country(),
        "latitude": float(fake.latitude()),
        "longitude": float(fake.longitude()),
        "zipcode": fake.postcode(),
        "street_address": fake.street_address(),
    }