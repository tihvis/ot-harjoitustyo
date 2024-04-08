import os
from dotenv import load_dotenv

dirname = os.path.dirname(__file__)

try:
    load_dotenv(dotenv_path=os.path.join(dirname, "..", ".env"))
except FileNotFoundError:
    pass

STUDYAPP_FILENAME = os.getenv("STUDYAPP_FILENAME") or "studyapp.sqlite"
STUDYAPP_FILE_PATH = os.path.join(dirname, "..", "data", STUDYAPP_FILENAME)
