import React from "react";

interface GameStatusProps {
  gameId: string;
  currentPlayer: number;
  gameOver: boolean;
  winner: number | null;
}

const GameStatus: React.FC<GameStatusProps> = ({
  gameId,
  currentPlayer,
  gameOver,
  winner,
}) => {
  return (
    <div className="game-status">
      <h2>Game ID: {gameId}</h2>
      {gameOver ? (
        <h2>Game Over! Winner: Player {winner}</h2>
      ) : (
        <h2>Current Turn: Player {currentPlayer}</h2>
      )}
    </div>
  );
};

export default GameStatus;
