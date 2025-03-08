import React, { useState, useEffect } from "react";
import axios from "axios";
import Header from "./components/Header";
import GameStatus from "./components/GameStatus";
import Board from "./components/Board";
import "./styles/App.css"; // Можно добавить дополнительные стили для App

const API_URL = "http://localhost:8000";

function App() {
  console.log("App is rendering!");
  const [gameId, setGameId] = useState(null);
  const [gameState, setGameState] = useState(null);

  // Функция для создания новой игры
  const createGame = async () => {
    try {
      const res = await axios.post(`${API_URL}/game/new`, { ai_vs_ai: false });
      setGameId(res.data.game_id);
    } catch (error) {
      console.error(error);
    }
  };

  // При наличии gameId получаем состояние игры
  useEffect(() => {
    if (!gameId) return;
    const fetchGameState = async () => {
      try {
        const res = await axios.get(`${API_URL}/game/${gameId}`);
        setGameState(res.data);
      } catch (error) {
        console.error(error);
      }
    };
    fetchGameState();
  }, [gameId]);

  // Обработка клика по клетке: стрелять можно только по полю противника
  const handleCellClick = async (row, col, boardOwner) => {
    if (!gameId || !gameState) return;
    // Предположим, что если current_player равен boardOwner, значит это своё поле — выстрел не выполняется.
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

  // Если игра ещё не создана, показываем кнопку создания игры
  if (!gameId) {
    return (
      <div className="app-container">
        <Header />
        <button onClick={createGame}>New Game</button>
      </div>
    );
  }

  // Если состояние игры не загружено
  if (!gameState) {
    return (
      <div className="app-container">
        <Header />
        <p>Loading game state...</p>
      </div>
    );
  }

  const { current_player, board1, board2, ships1, ships2, game_over, winner } = gameState;

  return (
    <div className="app-container">
      <Header />
      <GameStatus
        gameId={gameId}
        currentPlayer={current_player}
        gameOver={game_over}
        winner={winner}
      />
      <div className="boards">
        <div style={{ display: "flex", justifyContent: "space-around" }}>
          <div>
            <h3>Player 1 (Ships: {ships1})</h3>
            <Board
              boardData={board1}
              onCellClick={(row, col) => handleCellClick(row, col, 1)}
              isClickable={gameState.current_player !== 1 && !game_over}
            />
          </div>
          <div>
            <h3>Player 2 (Ships: {ships2})</h3>
            <Board
              boardData={board2}
              onCellClick={(row, col) => handleCellClick(row, col, 2)}
              isClickable={gameState.current_player !== 2 && !game_over}
            />
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;