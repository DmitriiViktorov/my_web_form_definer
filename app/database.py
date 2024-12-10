from motor.motor_asyncio import AsyncIOMotorClient

MONGO_DETAILS = "mongodb://db:27017"

client = AsyncIOMotorClient(MONGO_DETAILS)
database = client.forms
forms_collection = database.get_collection("forms")


