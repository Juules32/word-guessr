from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

view_router = APIRouter()
templates = Jinja2Templates(directory="templates")

@view_router.get("/")
def get_state():
    return RedirectResponse("/puzzles")

@view_router.get("/puzzles")
def get_puzzles(request: Request):
    return templates.TemplateResponse("views/puzzles.html", {"request": request})
