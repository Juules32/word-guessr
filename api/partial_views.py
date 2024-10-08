from typing import Any
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from core.game_manager import GameManager

partial_view_router = APIRouter()
templates = Jinja2Templates(directory="templates")
gm = GameManager()

def get_template_response(request: Request, file_path: str, data: Any):
    return templates.TemplateResponse(
        request=request, 
        name=file_path, 
        context={"request": request, "data": data}
    )

@partial_view_router.get("/htmx/puzzles")
def get_puzzles(request: Request, userid: str) -> HTMLResponse:
    data = gm.get_puzzles(userid)
    return get_template_response(request, "partial_views/puzzles.html", data)

@partial_view_router.get("/htmx/puzzles/{date}")
def get_puzzles(request: Request, date: str, userid: str, guess: str = None) -> HTMLResponse:
    if guess:
        gm.guess(date, userid, guess)
    data = gm.get_puzzle_state(date=date, userid=userid)
    return get_template_response(request, "partial_views/puzzle.html", data)

@partial_view_router.get("/htmx/stats")
def get_puzzles(request: Request, userid: str) -> HTMLResponse:
    data = gm.get_user_stats(userid)
    print(data)
    return get_template_response(request, "partial_views/stats.html", data)
