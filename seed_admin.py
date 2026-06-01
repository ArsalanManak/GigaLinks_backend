import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from passlib.context import CryptContext
import os
from dotenv import load_dotenv

load_dotenv()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def seed():
    uri = os.environ.get("MONGO_URI", "mongodb://localhost:27017")
    db_name = os.environ.get("DATABASE_NAME", "gigalinks")
    client = AsyncIOMotorClient(uri)
    db = client[db_name]

    email = "Gigalink00@gmail.com"
    existing = await db.users.find_one({"email": email})
    if existing:
        print(f"Admin user {email} already exists.")
    else:
        doc = {
            "name": "Admin",
            "email": email,
            "password_hash": pwd_context.hash("11223344"),
        }
        await db.users.insert_one(doc)
        print(f"Admin user {email} created successfully!")

    client.close()

if __name__ == "__main__":
    asyncio.run(seed())
