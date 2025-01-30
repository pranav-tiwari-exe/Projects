import { useState } from "react";

export default function App() {
  return (
    <>
      <Board />
    </>
  );
}

function Square({ value, onSquareClick }) {
  return (
    <button className="square" onClick={onSquareClick}>
      {value}
    </button>
  );
}

function Board() {
  const [Winner, setWinner] = useState(null);
  const [isXNext, setIsXNext] = useState(true);
  const [square, setSquare] = useState(Array(9).fill(null));

  const WinnerMessage = Winner ? Winner + " is the Winner!!!" : null;

  function handleClick(input) {
    const newSquareArray = square.slice();
    if (newSquareArray[input] === null && Winner === null) {
      newSquareArray[input] = isXNext ? "X" : "O";
      setIsXNext(!isXNext);
      setSquare(newSquareArray);
      checkWinner(newSquareArray);
    }
  }

  function checkWinner(squares) {
    const winLines = [
      [0, 1, 2],
      [3, 4, 5],
      [6, 7, 8],
      [0, 3, 6],
      [1, 4, 7],
      [2, 5, 8],
      [0, 4, 8],
      [2, 4, 6],
    ];

    for (let i = 0; i < winLines.length; i++) {
      const [a, b, c] = winLines[i];
      if (squares[a] === squares[b] && squares[c] === squares[b]) {
        setWinner(squares[a]);
      }
    }
  }

  function resetBoard() {
    setIsXNext(true);
    setSquare(Array(9).fill(null));
    setWinner(null);
  }

  return (
    <div className="container">
      <div className="board">
        <div className="board_row">
          <Square value={square[0]} onSquareClick={() => handleClick(0)} />
          <Square value={square[1]} onSquareClick={() => handleClick(1)} />
          <Square value={square[2]} onSquareClick={() => handleClick(2)} />
        </div>
        <div className="board_row">
          <Square value={square[3]} onSquareClick={() => handleClick(3)} />
          <Square value={square[4]} onSquareClick={() => handleClick(4)} />
          <Square value={square[5]} onSquareClick={() => handleClick(5)} />
        </div>
        <div className="board_row">
          <Square value={square[6]} onSquareClick={() => handleClick(6)} />
          <Square value={square[7]} onSquareClick={() => handleClick(7)} />
          <Square value={square[8]} onSquareClick={() => handleClick(8)} />
        </div>
      </div>

      <div>
        <button className="reset" onClick={resetBoard}>
          RESET
        </button>
      </div>
      <div className="winnerMessage">{WinnerMessage}</div>
    </div>
  );
}
