from fastapi import FastAPI
from faker import Faker
import random

app = FastAPI()
fake = Faker()

PRODUCT_CATEGORIES = [
    "Electronics",
    "Books",
    "Clothing",
    "Home & Kitchen",
    "Sports",
    "Beauty",
    "Toys",
]

BRANDS = [
    "TechPro",
    "SmartLife",
    "EcoPlus",
    "Nova",
    "PrimeGear",
    "UltraMax",
]




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





 