import React from "react";
import "./Board.css";

interface BoardProps {
  boardData: number[][];
  onCellClick: (rowIndex: number, colIndex: number) => void;
  isClickable: boolean;
}

const Board: React.FC<BoardProps> = ({ boardData, onCellClick, isClickable }) => {
  return (
    <div className="board-container">
      {/* Буквы для столбцов */}
      <div className="column-labels">
        <div className="label-corner"></div>
        {[...Array(boardData[0]?.length || 10)].map((_, i) => (
          <div key={`col-${i}`} className="column-label">
            {String.fromCharCode(65 + i)}
          </div>
        ))}
      </div>
      
      {/* Основное поле с номерами строк */}
      {boardData.map((row, rowIndex) => (
        <div className="board-row" key={rowIndex}>
          <div className="row-label">{rowIndex + 1}</div>
          {row.map((cellValue, colIndex) => {
            let cellClass = "cell";
            if (cellValue === 1) cellClass += " cell-ship";
            if (cellValue === 2) cellClass += " cell-hit";
            if (cellValue === 3) cellClass += " cell-miss";
            return (
              <div
                key={colIndex}
                className={cellClass}
                onClick={() => {
                  if (isClickable) onCellClick(rowIndex, colIndex);
                }}
              />
            );
          })}
        </div>
      ))}
    </div>
  );
};

export default Board;