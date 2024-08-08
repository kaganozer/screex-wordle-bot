import firebase_admin
from firebase_admin import db, credentials

import os
from dotenv import load_dotenv
load_dotenv()

cred = credentials.Certificate("database/credentials.json")

DATABASE_URL = os.getenv("DATABASE_URL")
firebase_admin.initialize_app(
    cred,
    {
        "databaseURL": DATABASE_URL
    },
)

ref = db.reference("/")


def get_node(node: str = ""):
    return db.reference(f"/{node}")
