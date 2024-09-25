# main.py

import os
from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.exceptions import HTTPException as StarletteHTTPException
from api.partial_views import partial_view_router
from api.views import view_router
from daily_puzzle_generation import generate_tomorrows_puzzle

# Custom path can be given to experiment locally with different env vars.
load_dotenv()

app = FastAPI()

templates = Jinja2Templates(directory="templates")

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(partial_view_router)

app.include_router(view_router)

# Custom 404 error handler
@app.exception_handler(StarletteHTTPException)
async def custom_404_handler(request: Request, exc: StarletteHTTPException):
    if exc.status_code == 404:
        return templates.TemplateResponse("errors/404.html", {"request": request}, status_code=404)
    return HTMLResponse(str(exc.detail), status_code=exc.status_code)

# Endpoint for daily cron event
@app.get("/cron/puzzle/generate")
def get_cron(request: Request) -> JSONResponse:
    authorization_header = request.headers.get("authorization")

    if not authorization_header:
        return JSONResponse({"error": "Missing authorization header"}, status_code=401)

    if authorization_header != f"Bearer {os.getenv("CRON_SECRET")}":
        return JSONResponse({"error": "Invalid authorization header"}, status_code=403)

    else:
        generate_tomorrows_puzzle()
        return JSONResponse({"result": "success"})
