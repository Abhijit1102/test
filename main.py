from fastapi import FastAPI
from faker import Faker

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


# @app.get("/product")
# def get_random_product():
#     return {
#         "product_name": fake.word(),
#         "price": round(fake.random_number(digits=3) + 0.99, 2),
#         "description": fake.sentence(),
#     }