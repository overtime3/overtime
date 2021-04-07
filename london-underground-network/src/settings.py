from dotenv import load_dotenv
import os

load_dotenv(verbose=True)

API_KEY = os.getenv("API_KEY")

##########################
# Provide API key for TFL API
# Create .env file and insert one constant which is 'API_KEY={insert_your_API_key}'
##########################