from flask import Flask, render_template, request
import chess
import chess.pgn
import chess.svg
import json
from io import StringIO

app = Flask(__name__)

def render_svg(svg, current_move):
    svg = svg.replace('<svg', '<svg data-move={}'.format(current_move))
    return svg


# Initialize current_move outside of the index route
current_move = 0

@app.route('/', methods=['GET', 'POST'])
def index():
    global current_move  # Access the global current_move variable
    move = ''
    moves = []
    current_move_player = ''
    current_move_san = ''
    # Inside your Flask route
    if request.method == 'POST':
        pgn_data = request.form['pgn_data']
        game = chess.pgn.read_game(StringIO(pgn_data))

        if game is None:
            return render_template('index.html', error_message="Invalid PGN data. Please check your input.")

        headers = game.headers
        board = chess.Board()
        moves = list(game.mainline_moves())

        # Calculate the total number of moves
        total_moves = len(moves)

        # Inside your Flask route
        if 'prev_move' in request.form:
            if current_move > 0:
                current_move -= 1
                current_move_player = 'White' if current_move % 2 == 0 else 'White'
                current_move_san = board.san(moves[current_move-1])
                board = update_board(moves, current_move)
                move = str(moves[current_move])
                
        elif 'next_move' in request.form:
            if current_move < len(moves):
                current_move += 1
                current_move_player = 'White' if current_move % 2 == 0 else 'White'
                current_move_san = board.san(moves[current_move-1])
                board = update_board(moves, current_move)
                move = str(moves[current_move])
                
        else:
            # When initially rendering the template, you should pass an empty list for moves
            board = chess.Board()
            current_move = 0
            move = ''
            current_move_player = ''
            current_move_san = ''
        
        # Convert moves to a list of move strings
        move_strings = [str(move) for move in moves]
        # Render the board to show the current move
        board_svg = chess.svg.board(board=board, lastmove=moves[current_move-1] if current_move < len(moves) else None, arrows=[chess.svg.Arrow(moves[current_move-1].from_square, moves[current_move-1].to_square)], coordinates=True, size=400)
        return render_template('index.html', headers=headers, board_svg=render_svg(board_svg,current_move), current_move=current_move, pgn_data=pgn_data, total_moves=total_moves, move=move,moves=move_strings, current_move_player=current_move_player, current_move_san=current_move_san)
    
    move_strings = [str(move) for move in moves]
    return render_template('index.html',moves=json.dumps(move_strings))

def update_board(moves, move_number):
    board = chess.Board()
    for move in moves[:move_number]:
        board.push(move)
    return board

if __name__ == '__main__':
    app.run(debug=True)
