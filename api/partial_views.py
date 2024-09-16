from typing import Any
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from core.game_manager import GameManager
from db.kv_manager import KeyValueManager

partial_view_router = APIRouter()
templates = Jinja2Templates(directory="templates")
gm = GameManager(kv=KeyValueManager())

def get_template_response(request: Request, file_path: str, data: Any):
    return templates.TemplateResponse(
        request=request, 
        name=file_path, 
        context={"request": request, "data": data}
    )

@partial_view_router.put("/htmx/{date}/{userid}/{guess}")
def put_guess(request: Request, date: str, userid: str, guess: str) -> HTMLResponse:
    gm.guess(date, userid, guess)
    data = gm.get_puzzle_state(date, userid)
    return get_template_response(request, "partial_views/placeholder.html", data)

@partial_view_router.get("/htmx/puzzles")
def get_puzzles(request: Request) -> HTMLResponse:
    userid = "user_1" # Should be changed to be generated and stored locally
    data = gm.get_puzzles(userid)
    return get_template_response(request, "partial_views/puzzles.html", data)

@partial_view_router.get("/htmx/puzzles/{date}")
def get_puzzles(request: Request, date: str, userid: str) -> HTMLResponse:
    data = gm.get_puzzle_state(date=date, userid=userid)
    return get_template_response(request, "partial_views/puzzle.html", data)
