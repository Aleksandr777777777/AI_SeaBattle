import React from "react";
import "../styles/Board.css";

interface BoardProps {
  boardData: number[][];
  onCellClick: (rowIndex: number, colIndex: number) => void;
  isClickable: boolean;
}

const Board: React.FC<BoardProps> = ({ boardData, onCellClick, isClickable }) => {
  return (
    <div className="board">
      {boardData.map((row, rowIndex) => (
        <div className="board-row" key={rowIndex}>
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
