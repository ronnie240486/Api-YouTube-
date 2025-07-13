import os
from dotenv import load_dotenv

load_dotenv()

AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY")
AWS_SECRET_KEY = os.getenv("AWS_SECRET_KEY")
ASSOCIATE_TAG = os.getenv("ASSOCIATE_TAG")
REGION = os.getenv("REGION")
MARKETPLACE = os.getenv("MARKETPLACE")