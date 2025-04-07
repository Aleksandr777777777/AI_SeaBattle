import { useState } from 'react';
import PixelShips from './PixelShips';
import TransitionAnimation from './TransitionAnimation';
import './MainMenu.css';

const MainMenu = ({ onCreateGame }: { onCreateGame: () => void }) => {
  const [transition, setTransition] = useState(false);

  const handleNewGame = () => {
    setTransition(true);
  };

  return (
    <div className="main-menu">
      <PixelShips />
      
      {transition ? (
        <TransitionAnimation onComplete={onCreateGame} />
      ) : (
        <div className="menu-content">
          <h1 className="game-title">AI SeaBattle</h1>
          <button className="neon-button" onClick={handleNewGame}>
            NEW GAME
          </button>
        </div>
      )}
    </div>
  );
};

export default MainMenu;