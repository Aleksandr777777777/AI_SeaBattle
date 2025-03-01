// src/Board.jsx
import React from "react";
import "./Board.css";

function Board({boardData, onCellClick}) {
  return (
    <div className="board">
      {boardData.map((row, rowIndex) => (
        <div className="board-row" key={rowIndex}>
          {row.map((cellValue, colIndex) => {
            // Отобразим символы в зависимости от cellValue
            // 0=пусто, 1=корабль, 2=попадание, 3=промах
            let display = "";
            switch (cellValue) {
              case 0:
                display = "";
                break;
              case 1:
                // Если хотим скрыть корабли противника, 
                // надо будет проверять, чей это борт
                display = "S"; 
                break;
              case 2:
                display = "X"; 
                break;
              case 3:
                display = "•"; 
                break;
              default:
                display = cellValue;
            }
            return (
              <div
                key={colIndex}
                className="board-cell"
                onClick={() => onCellClick(rowIndex, colIndex)}
              >
                {display}
              </div>
            );
          })}
        </div>
      ))}
    </div>
  );
}

export default Board;
