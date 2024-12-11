from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import ASCENDING

MONGO_DETAILS = "mongodb://db:27017"

client = AsyncIOMotorClient(MONGO_DETAILS)
database = client.forms
forms_collection = database.get_collection("forms")


async def initialize_database():

    # await database.get_collection("forms").drop()
    if await forms_collection.count_documents({}) == 0:
        print("Initializing database...")
        await forms_collection.create_index([("name", ASCENDING)], unique=True)
        test_data = [
            {
                "name": "User authentication",
                "email": "email",
                "username": "text"
            },
            {
                "name": "User login",
                "email": "email",
                "password": "text"
            },
            {
                "name": "User profile",
                "full_name": "text",
                "birth_date": "date",
                "email": "email",
            },
            {
                "name": "Discount params",
                "description": "text",
                "date_from": "date",
                "date_to": "date",
                "discount": "text",
            }
        ]

        await forms_collection.insert_many(test_data)
