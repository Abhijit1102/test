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


@app.get("/product")
def get_random_product():
    categories = [
        "Electronics",
        "Books",
        "Clothing",
        "Furniture",
        "Sports",
        "Beauty"
    ]

    return {
        "id": fake.uuid4(),
        "name": fake.word().title() + " " + fake.word().title(),
        "category": random.choice(categories),
        "price": round(random.uniform(10, 5000), 2),
        "description": fake.sentence(),
        "brand": fake.company(),
        "stock": random.randint(0, 100),
    }