import os
from dotenv import load_dotenv

load_dotenv()
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS","http://localhost:8000").split(",")