from fastapi import FastAPI
from alembic.config import Config
from alembic import command
from scripts.data_populated_script import populate_data
import time

from src.routes import table_router


def run_migrations():
    alembic_cfg = Config("./alembic.ini")  # Path to your Alembic configuration file
    command.upgrade(alembic_cfg, "head")


time.sleep(5)
run_migrations()
populate_data()

# Create an instance of the FastAPI class
app = FastAPI()


# Define a route and a handler function
@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}


app.include_router(table_router.router, prefix="/api/v1")
