from pymongo import MongoClient
from pymongo.server_api import ServerApi
from . import get_settings, Settings
from fastapi import Depends


def connect_mongodb(app_settings: Settings = (get_settings())):
    if not app_settings.MONGODB_URI:
        raise ValueError("MONGODB_URI is not configured")

    client = MongoClient(app_settings.MONGODB_URI, server_api=ServerApi("1"))
    try:
        client.admin.command("ping")
        print("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        print(e)
        raise

    return client
