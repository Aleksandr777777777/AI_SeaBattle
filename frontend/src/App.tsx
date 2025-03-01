// src/App.jsx
import React, {useState, useEffect} from "react";
import axios from "axios";
import Board from "./Board";

const API_URL = "http://localhost:8000";

function App() {
  const [gameId, setGameId] = useState(null);
  const [gameState, setGameState] = useState(null);

  // Создаем игру
  const createGame = async () => {
    try {
      const res = await axios.post(`${API_URL}/game/new`, { ai_vs_ai: true });
      setGameId(res.data.game_id);
    } catch (error) {
      console.error(error);
    }
  };

  // Когда появился gameId, запрашиваем состояние
  useEffect(() => {
    if (!gameId) return;
    if (gameState) {
      console.log("Полученное состояние игры:", gameState);
    }
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

  // Функция для обработки хода
  const makeMove = async (row, col) => {
    if (!gameId) return;
    try {
      const res = await axios.post(`${API_URL}/game/${gameId}/move`, {
        row,
        col,
      });
      setGameState(res.data);
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <div>
      <h1>Battleship AI</h1>
      <button onClick={createGame}>New Game (AI vs AI)</button>
      {gameState && (
        <div style={{ display: "flex", justifyContent: "space-around" }}>
          <div>
            <h2>Player 1 (ships: {gameState.ships1})</h2>
            <Board boardData={gameState.board1} onCellClick={makeMove} />
          </div>
          <div>
            <h2>Player 2 (ships: {gameState.ships2})</h2>
            <Board boardData={gameState.board2} onCellClick={makeMove} />
          </div>
        </div>
      )}
    </div>
  );
}

export default App;
