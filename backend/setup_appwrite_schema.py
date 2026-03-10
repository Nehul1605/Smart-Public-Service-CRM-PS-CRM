import os
import sys
from dotenv import load_dotenv
from appwrite.client import Client
from appwrite.services.databases import Databases
from appwrite.exception import AppwriteException

# Load environment variables
load_dotenv()

ENDPOINT      = os.getenv("APPWRITE_ENDPOINT", "https://cloud.appwrite.io/v1")
PROJECT_ID    = os.getenv("APPWRITE_PROJECT_ID")
API_KEY       = os.getenv("APPWRITE_API_KEY")
DATABASE_ID   = os.getenv("APPWRITE_DATABASE_ID", "civicpulse_db")
COLLECTION_ID = os.getenv("APPWRITE_COLLECTION_ID", "complaints")

if not PROJECT_ID or not API_KEY:
    print("Error: APPWRITE_PROJECT_ID and APPWRITE_API_KEY must be set in .env")
    sys.exit(1)

client = Client()
client.set_endpoint(ENDPOINT)
client.set_project(PROJECT_ID)
client.set_key(API_KEY)

databases = Databases(client)

attributes = [
    {"id": "reporterName", "type": "string", "size": 100, "required": False},
    {"id": "reporterId", "type": "string", "size": 100, "required": False},
    {"id": "priorityScore", "type": "float", "required": False},
    {"id": "slaHours", "type": "integer", "required": False},
    {"id": "slaRemainingHours", "type": "integer", "required": False},
    {"id": "state", "type": "string", "size": 100, "required": False},
]

def setup_attributes():
    print(f"Starting schema update for collection: {COLLECTION_ID} in database: {DATABASE_ID}")
    
    for attr in attributes:
        try:
            print(f"Adding attribute '{attr['id']}'...")
            if attr["type"] == "string":
                databases.create_string_attribute(
                    database_id=DATABASE_ID,
                    collection_id=COLLECTION_ID,
                    key=attr["id"],
                    size=attr["size"],
                    required=attr["required"]
                )
            elif attr["type"] == "integer":
                databases.create_integer_attribute(
                    database_id=DATABASE_ID,
                    collection_id=COLLECTION_ID,
                    key=attr["id"],
                    required=attr["required"]
                )
            elif attr["type"] == "float":
                databases.create_float_attribute(
                    database_id=DATABASE_ID,
                    collection_id=COLLECTION_ID,
                    key=attr["id"],
                    required=attr["required"]
                )
            print(f"Successfully added '{attr['id']}'")
        except AppwriteException as e:
            if "already exists" in str(e).lower():
                print(f"Attribute '{attr['id']}' already exists. Skipping.")
            else:
                print(f"Failed to add '{attr['id']}': {str(e)}")

if __name__ == "__main__":
    setup_attributes()
    print("Schema update complete.")
