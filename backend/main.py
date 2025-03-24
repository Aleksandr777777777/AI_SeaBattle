# backend/main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uuid
from game import Game
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,   # Можно указать ["*"] для теста
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
games = {}  # game_id -> Game

class MoveRequest(BaseModel):
    row: int
    col: int

@app.get("/")
def root():
    return {"message": "Battleship AI API is running!"}

@app.post("/game/new")
def new_game(ai_vs_ai: bool = True):
    """Создать новую игру. Возвращаем game_id."""
    game_id = str(uuid.uuid4())
    game = Game(game_id=game_id, ai_vs_ai=ai_vs_ai)
    games[game_id] = game
    return {"game_id": game_id}

@app.get("/game/{game_id}")
def get_game_state(game_id: str):
    """Получить текущее состояние игры."""
    if game_id not in games:
        raise HTTPException(status_code=404, detail="Game not found")

    game = games[game_id]

    return {
        "game_id": game.game_id,
        "board1": game.board1,
        "board2": game.board2,
        "current_player": game.current_player,
        "ships1": game.ships1,
        "ships2": game.ships2,
        "game_over": game.game_over,
        "winner": game.winner
    }

@app.post("/game/{game_id}/move")
def make_move(game_id: str, move: MoveRequest):
    """Сделать ход в игру."""
    if game_id not in games:
        raise HTTPException(status_code=404, detail="Game not found")

    game = games[game_id]

    if game.game_over:
        return {"message": "Game is over"}

    game.make_move(move.row, move.col)

    return {
        "board1": game.board1,
        "board2": game.board2,
        "current_player": game.current_player,
        "ships1": game.ships1,
        "ships2": game.ships2,
        "game_over": game.game_over,
        "winner": game.winner
    }
    
@app.post("/game/{game_id}/ai_move")
def ai_move(game_id: str):
    """Сделать ход агента (игрок 2)."""
    if game_id not in games:
        raise HTTPException(status_code=404, detail="Game not found")
    
    game = games[game_id]
    if game.game_over:
        return {"message": "Game is over"}

    move_result = game.ai_move()
    if move_result is None:
        return {"message": "No AI move performed"}
    
    row, col, result = move_result
    return {
        "board1": game.board1,
        "board2": game.board2,
        "current_player": game.current_player,
        "ships1": game.ships1,
        "ships2": game.ships2,
        "game_over": game.game_over,
        "winner": game.winner,
        "ai_move": {"row": row, "col": col, "result": result}
    }
