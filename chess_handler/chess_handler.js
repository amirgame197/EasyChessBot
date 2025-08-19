const Chess = require('chess.js').Chess;
const readline = require('readline');
const chess = new Chess();

const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout
});

let stageLog = ''; 

function addToStageLog(message) {
  stageLog += message + ' ';
}

function printStageLog() {
  console.log(stageLog.trim());
  stageLog = '';
}

function printCustomBoard() {
  const rows = [];
  const board = chess.board();
  for (let i = 0; i < board.length; i++) {
    for (let j = 0; j < board[i].length; j++) {
      const square = String.fromCharCode(97 + j) + (8 - i);
      if (board[i][j] === null) {
        rows.push(`${square}:solid`);
      } else {
        const piece = getFullPieceName(board[i][j].type);
        const color = board[i][j].color === 'w' ? 'W' : 'B';
        rows.push(`${square}:${piece}:${color}`);
      }
    }
  }
  addToStageLog(rows.join(' '));
  printStageLog();
}

function getFullPieceName(piece) {
  switch (piece) {
    case 'p': return 'pawn';
    case 'r': return 'rook';
    case 'n': return 'knight';
    case 'b': return 'bishop';
    case 'q': return 'queen';
    case 'k': return 'king';
    default: return 'unknown';
  }
}

function listMoves(square) {
  const moves = chess.moves({ square: square, verbose: true });
  if (moves.length === 0) {
    addToStageLog('No legal moves for this piece. | ');
    promptPiecePosition();
  } else {
    const movesStr = moves.map(move => `${move.to}#${chess.turn()}`).join('&');
    addToStageLog(`~${movesStr}~`);
    promptMove(square);
  }
  printStageLog();
}

function promptPiecePosition() {
  rl.question(`Player ${chess.turn() === 'w' ? 'White' : 'Black'}, pickup your piece: | `, (square) => {
    if (!chess.get(square)) {
      addToStageLog('No piece at this position, please try again. | ');
      printStageLog();
      promptPiecePosition();
    } else {
      listMoves(square);
    }
  });
}

function promptMove(square) {
  rl.question('No way back now! Choose the destination square: | ', (destination) => {
    const legalMoves = chess.moves({ square: square, verbose: true });
    const isLegalMove = legalMoves.some(m => m.to === destination);
    if (!isLegalMove) {
      addToStageLog(`Invalid move, please try again. | `);
      promptMove(square);
    } else {
      const isPromotion = (chess.get(square).type === 'p' &&
                           (destination[1] === '8' || destination[1] === '1'));
      const promotionPiece = isPromotion ? 'q' : null

      const moveResult = chess.move({ from: square, to: destination, promotion: promotionPiece });
      if (moveResult === null) {
        addToStageLog('Invalid move, please try again. | ');
        listMoves(square);
      } else {
        printCustomBoard();
        checkGameStatus();
      }
      printStageLog();
    }
    printStageLog();
  });
}


function checkGameStatus() {
  if (chess.isCheckmate()) {
    addToStageLog('Checkmate! Game over. | ');
    rl.close();
  } else if (chess.isDraw()) {
    addToStageLog('Draw! Game over. | ');
    rl.close();
  } else if (chess.isStalemate()) {
    addToStageLog('Stalemate! Game over. | ');
    rl.close();
  } else if (chess.isThreefoldRepetition()) {
    addToStageLog('Threefold repetition! Game over. | ');
    rl.close();
  } else if (chess.isInsufficientMaterial()) {
    addToStageLog('Insufficient material! Game over. | ');
    rl.close();
  } else {
    promptPiecePosition();
  }
  printStageLog();
}

printCustomBoard();
promptPiecePosition();
