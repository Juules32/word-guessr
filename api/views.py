from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from util.date import get_date_str

view_router = APIRouter()
templates = Jinja2Templates(directory="templates")

@view_router.get("/")
def get_puzzle_state():
    return RedirectResponse(f"/puzzles/{get_date_str()}")

@view_router.get("/puzzles")
def get_puzzles(request: Request):
    return templates.TemplateResponse("views/puzzles.html", {"request": request})

@view_router.get("/puzzles/{date}")
def get_puzzles(request: Request, date: str):
    userid = "user_1"
    return templates.TemplateResponse("views/puzzle.html", {"request": request, "date": date, "userid": userid})
