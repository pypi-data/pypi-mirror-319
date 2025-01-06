import os

from dotenv import load_dotenv
from sqlmodel import create_engine

load_dotenv()

USER_DB = os.getenv("USER_DB")
PASS_DB = os.getenv("PASS_DB")
HOST_DB = os.getenv("HOST_DB")
PORT_DB = os.getenv("PORT_DB")
NAME_DB = os.getenv("NAME_DB")

DATABASE_URL = f"postgresql://{USER_DB}:{PASS_DB}@{HOST_DB}:{PORT_DB}/{NAME_DB}"

engine = create_engine(DATABASE_URL, echo=True)
