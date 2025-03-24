import React, { useState, useEffect } from "react";
import axios from "axios";
import Header from "./components/Header";
import GameStatus from "./components/GameStatus";
import Board from "./components/Board";
import "./styles/App.css";

const API_URL = "http://localhost:8000";

interface GameState {
  game_id: string;
  board1?: number[][]; // делаем опциональными, чтобы учесть, что могут отсутствовать
  board2?: number[][];
  current_player?: number;
  ships1?: number;
  ships2?: number;
  game_over?: boolean;
  winner?: number | null;
  message?: string;
}

const App: React.FC = () => {
  console.log("App is rendering!");
  const [gameId, setGameId] = useState<string | null>(null);
  const [gameState, setGameState] = useState<GameState | null>(null);

  const createGame = async () => {
    try {
      const res = await axios.post(`${API_URL}/game/new`, { ai_vs_ai: false });
      setGameId(res.data.game_id);
    } catch (error) {
      console.error(error);
    }
  };

  const fetchGameState = async () => {
    if (!gameId) return;
    try {
      const res = await axios.get(`${API_URL}/game/${gameId}`);
      setGameState(res.data);
    } catch (error) {
      console.error(error);
    }
  };

  useEffect(() => {
    if (gameId) {
      fetchGameState();
    }
  }, [gameId]);

  const handleCellClick = async (row: number, col: number, boardOwner: number) => {
    if (!gameId || !gameState) return;
    // Если current_player равен boardOwner, значит, выстрел по своему полю не выполняется.
    if (gameState.current_player === boardOwner) {
      console.log("Cannot shoot on your own board!");
      return;
    }
    try {
      const res = await axios.post(`${API_URL}/game/${gameId}/move`, { row, col });
      setGameState(res.data);
    } catch (error) {
      console.error(error);
    }
  };

  const handleAIMove = async () => {
    if (!gameId) return;
    try {
      const res = await axios.post(`${API_URL}/game/${gameId}/ai_move`);
      setGameState(res.data);
    } catch (error) {
      console.error(error);
    }
  };

  // Если игра ещё не создана
  if (!gameId) {
    return (
      <div className="app-container">
        <Header />
        <button onClick={createGame}>New Game (Human vs Agent)</button>
      </div>
    );
  }

  // Если состояние игры не загружено или сервер вернул сообщение (например, игра окончена)
  if (!gameState || !gameState.board1 || !gameState.board2) {
    return (
      <div className="app-container">
        <Header />
        {gameState?.message ? (
          <p>{gameState.message}</p>
        ) : (
          <p>Loading game state...</p>
        )}
      </div>
    );
  }

  const { current_player, board1, board2, ships1, ships2, game_over, winner } = gameState;

  return (
    <div className="app-container">
      <Header />
      <GameStatus
        gameId={gameId}
        currentPlayer={current_player!}
        gameOver={game_over!}
        winner={winner!}
      />
      <div className="boards">
        <div style={{ display: "flex", justifyContent: "space-around" }}>
          {/* Поле игрока 1 (Human) — не кликабельно */}
          <div>
            <h3>Player 1 (Human) (Ships: {ships1})</h3>
            <Board
              boardData={board1}
              onCellClick={() => {}}
              isClickable={false}
            />
          </div>
          {/* Поле игрока 2 (Agent) — кликабельно, если сейчас ход human */}
          <div>
            <h3>Player 2 (Agent) (Ships: {ships2})</h3>
            <Board
              boardData={board2}
              onCellClick={(r, c) => handleCellClick(r, c, 2)}
              isClickable={current_player === 1 && !game_over}
            />
          </div>
        </div>
      </div>
      {/* Если сейчас ход агента */}
      {current_player === 2 && !game_over && (
        <button onClick={handleAIMove}>Agent Move</button>
      )}
    </div>
  );
};

export default App;
