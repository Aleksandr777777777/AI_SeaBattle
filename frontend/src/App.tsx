import React, { useState, useEffect } from "react";
import axios from "axios";
import Header from "./components/Header/Header";
import Board from "./components/Board/Board";
import MainMenu from "./components/MainMenu/MainMenu";
import "./styles/App.css";

const API_URL = "http://localhost:8000";

interface GameState {
  game_id: string;
  board1?: number[][];
  board2?: number[][];
  current_player?: number;
  ships1?: number;
  ships2?: number;
  game_over?: boolean;
  winner?: number | null;
  message?: string;
}

const App: React.FC = () => {
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

  // Главный рендер
  if (!gameId) {
    return <MainMenu onCreateGame={createGame} />;
  }

  if (!gameState || !gameState.board1 || !gameState.board2) {
    return (
      <div className="app-container">
        <Header />
        {gameState?.message ? <p>{gameState.message}</p> : <p>Loading...</p>}
      </div>
    );
  }

  const {current_player, board1, board2, ships1, ships2, game_over, winner} = gameState;

  return (
    <div className="app-container">
      <Header 
        gameId={gameId}
        currentPlayer={current_player}
        ships1={ships1}
        ships2={ships2}
      />
      
      <div className="boards-container">
        <div className="player-board">
          <Board boardData={board1} onCellClick={() => {}} isClickable={false} />
        </div>
  
        <div className="player-board">
          <Board
            boardData={board2}
            onCellClick={(r, c) => handleCellClick(r, c, 2)}
            isClickable={current_player === 1 && !game_over}
          />
        </div>
      </div>
  
      {current_player === 2 && !game_over && (
      <div className="button-container">
        <button className="wave-button" onClick={handleAIMove}>
          <span>🌊 AI Move 🌊</span>
          <div className="wave"></div>
        </button>
      </div>
      )}
    </div>
  );
};

export default App;