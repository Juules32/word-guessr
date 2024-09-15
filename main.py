# main.py

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from api.partial_views import partial_view_router
from api.views import view_router

# Custom path can be given to experiment locally with different env vars.
load_dotenv()

app = FastAPI()

# app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(partial_view_router)

app.include_router(view_router)
