from fastapi import FastAPI
from faker import Faker
import random

app = FastAPI()
fake = Faker()

PRODUCT_CATEGORIES = [
    "Laptop",
    "Smartphone",
    "Headphones",
    "Keyboard",
    "Mouse",
    "Monitor",
    "Smartwatch",
    "Camera",
    "Tablet",
    "Gaming Console",
]

BRANDS = [
    "Apple",
    "Samsung",
    "Sony",
    "Dell",
    "HP",
    "Lenovo",
    "Asus",
    "Logitech",
    "Microsoft",
    "Acer",
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


@app.get("/product")
def get_random_product():
    brand = random.choice(BRANDS)
    category = random.choice(PRODUCT_CATEGORIES)

    return {
        "id": fake.uuid4(),
        "name": f"{brand} {category}",
        "brand": brand,
        "category": category,
        "price": round(random.uniform(50, 5000), 2),
        "currency": "USD",
        "sku": fake.bothify(text="???-#####"),
        "in_stock": random.choice([True, False]),
        "rating": round(random.uniform(1, 5), 1),
        "description": fake.sentence(),
    }