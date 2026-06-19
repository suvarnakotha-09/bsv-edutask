import os
import pytest
import pymongo
from dotenv import dotenv_values
from src.util.dao import DAO

DATABASE_NAME = "integration_test_db"

USER_SCHEMA = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["firstName", "lastName", "email"],
        "properties": {
            "firstName": {"bsonType": "string"},
            "lastName": {"bsonType": "string"},
            "email": {"bsonType": "string"}
        }
    }
}


@pytest.fixture(scope="session")
def mongo_connection_url():
    env_url = dotenv_values(".env").get("MONGO_URL")
    return os.environ.get("MONGO_URL", env_url) or "mongodb://localhost:27017"


@pytest.fixture(scope="session")
def mongo_client(mongo_connection_url):
    client = pymongo.MongoClient(mongo_connection_url)
    yield client
    client.close()


@pytest.fixture(scope="session")
def integration_database(mongo_client):

    database = mongo_client[DATABASE_NAME]

    if "user" in database.list_collection_names():
        database.drop_collection("user")

    database.create_collection(
        "user",
        validator=USER_SCHEMA
    )

    yield database

    mongo_client.drop_database(DATABASE_NAME)


@pytest.fixture
def clean_user_collection(integration_database):

    user_collection = integration_database["user"]

    user_collection.delete_many({})
    yield
    user_collection.delete_many({})


@pytest.fixture
def user_dao(integration_database, clean_user_collection):

    dao_instance = DAO.__new__(DAO)
    dao_instance.collection = integration_database["user"]

    return dao_instance