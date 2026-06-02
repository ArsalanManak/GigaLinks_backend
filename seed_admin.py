import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import bcrypt
import os
from dotenv import load_dotenv

load_dotenv()

async def seed():
    uri = os.environ.get("MONGO_URI", "mongodb://localhost:27017")
    db_name = os.environ.get("DATABASE_NAME", "gigalinks")
    client = AsyncIOMotorClient(uri)
    db = client[db_name]

    email = "Gigalink00@gmail.com"
    hashed = bcrypt.hashpw("11223344".encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
    
    existing = await db.users.find_one({"email": email})
    if existing:
        await db.users.update_one({"email": email}, {"$set": {"password_hash": hashed}})
        print(f"Admin user {email} already exists. Password updated successfully!")
    else:
        doc = {
            "name": "Admin",
            "email": email,
            "password_hash": hashed,
        }
        await db.users.insert_one(doc)
        print(f"Admin user {email} created successfully!")

    client.close()

if __name__ == "__main__":
    asyncio.run(seed())
