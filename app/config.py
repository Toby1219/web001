import os
from datetime import timedelta
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRETE_KEY")
    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI")
    SQLALCHEMY_TRACK_MODIFICATION = os.getenv("SQLALCHEMY_TRACK_MODIFICATION")
    REMEMBER_COOKIE_DURATION = timedelta(days=int(os.getenv("REMEMBER_COOKIE_DURATION")))
    
    ADMIN_NAME = os.getenv("ADMIN_NAME")
    PASSKEY = os.getenv("PASSKEY")
    WALLET_TYPE = os.getenv("WALLET_TYPE")
    WALLET_ADDRESS = os.getenv("WALLET_ADDRESS")

   
    
    
    