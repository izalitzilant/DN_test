import os

from dotenv import load_dotenv

load_dotenv()

FILESTORE_DIR = os.getenv("FILESTORE_DIR")

if not os.path.exists(FILESTORE_DIR):
        os.mkdir(FILESTORE_DIR)

def get_filestore_dir():
    return FILESTORE_DIR

PORT_NUMBER = os.getenv("PORT_NUMBER")


