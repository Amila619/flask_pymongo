from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()
uri = os.getenv('URI')

def get_db():
    try:
        client = MongoClient(
            uri,
            tls=True,
            tlsAllowInvalidCertificates=False
        )
        return client.demo
    except Exception as e:
        raise Exception("Unable to connect to database due to", e)