from typing import Any
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from core.game_manager import GameManager
from db.kv_manager import KeyValueManager

api_router = APIRouter()
templates = Jinja2Templates(directory="templates")
gm = GameManager(kv=KeyValueManager())

def get_template_response(request: Request, file_path: str, data: Any):
    return templates.TemplateResponse(
        request=request, 
        name=file_path, 
        context={"request": request, "data": data}
    )

@api_router.get("/api/{date}/{userid}")
def get_state(request: Request, date: str, userid: str) -> HTMLResponse:
    data = gm.get_state(date, userid)
    return get_template_response(request, "placeholder.html", data)

@api_router.put("/api/{date}/{userid}/{guess}")
def put_guess(request: Request, date: str, userid: str, guess: str) -> HTMLResponse:
    gm.guess(date, userid, guess)
    data = gm.get_state(date, userid)
    return get_template_response(request, "placeholder.html", data)

@api_router.get("/api/puzzle_list")
def get_puzzles(request: Request) -> None:
    userid = "user_1" # Should be changed to be generated and stored locally
    data = gm.get_puzzles(userid)
    print(data)
    return get_template_response(request, "puzzle_list.html", data)
