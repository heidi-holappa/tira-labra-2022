import os
from dotenv import load_dotenv

dirname = os.path.dirname(__file__)

try:
    load_dotenv(dotenv_path=os.path.join(dirname, '..', '.env'))
except FileNotFoundError:
    print("Warning! .env file not found.")

path = os.getenv('DEFAULT_DATA_DIRECTORY') or 'data'

DEFAULT_DATA_PATH = os.path.join(dirname, '..', path)
