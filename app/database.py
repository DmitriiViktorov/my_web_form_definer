from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import ASCENDING

MONGO_DETAILS = "mongodb://db:27017"

client = AsyncIOMotorClient(MONGO_DETAILS)
database = client.forms
forms_collection = database.get_collection("forms")

test_collection = database.get_collection("test")


async def initialize_database(collection):

    # await database.get_collection("forms").drop()
    if await collection.count_documents({}) == 0:
        print("Initializing database...")
        await collection.create_index([("name", ASCENDING)], unique=True)
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

        await collection.insert_many(test_data)
