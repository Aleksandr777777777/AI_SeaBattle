import React from "react";
import "./Header.css";

interface HeaderProps {
  gameId?: string;
  currentPlayer?: number;
  ships1?: number;
  ships2?: number;
}

const Header: React.FC<HeaderProps> = ({ gameId, currentPlayer, ships1, ships2 }) => {
  return (
    <header className="game-header">
      <h1 className="game-title">AI SeaBattle</h1>
      
      {gameId && (
        <div className="game-meta">
          <div className="game-id">Game ID: {gameId}</div>
          
          <div className={`turn-indicator ${currentPlayer === 1 ? 'your-turn' : 'ai-turn'}`}>
            {currentPlayer === 1 ? (
              <>🎯 <strong>Your Turn</strong> - Click on AI's board to attack</>
            ) : (
              <>🤖 <strong>AI is Thinking</strong> - Please wait...</>
            )}
          </div>

          <div className="ships-info">
            <span className="player-ships">🚢 Your ships: {ships1}</span>
            <span className="ai-ships">🤖 AI ships: {ships2}</span>
          </div>
        </div>
      )}
    </header>
  );
};

export default Header;