import streamlit as st
import chess
import chess.pgn
import chess.engine
import chess.svg
from io import StringIO

# Title of the Web App
st.title("Chess PGN Analysis")

# Subtitle of the Web App
st.subheader("Web App to Analyze and Read a Chess Game from PGN Data")

# Text Heading for the PGN Data
st.subheader("Upload the PGN Data")

# Radio button to choose between pasting the data or uploading a file
pgn_input_type = st.radio(
    "Choose an input method:",
    ("Paste the data", "Upload a file")
)

# Initialize the input variables
pgn_data = ""
pgn_file = None

# Input types based on the radio button
if pgn_input_type == "Paste the data":
    # Text Area to paste the PGN Data
    pgn_data = st.text_area("Paste the PGN Data here")
else:
    # File Uploader to upload the PGN Data with type .pgn
    pgn_file = st.file_uploader("Upload the PGN File here", type=['pgn'])

# Check if the given input is not empty and then show the continue button
if (pgn_input_type == "Paste the data" and pgn_data.strip() != "") or (pgn_input_type == "Upload a file" and pgn_file is not None):
    # Continue Button
    if st.button("Continue") or True:
        # If the input type is "Paste the data," read the data from the text area
        if pgn_input_type == "Paste the data":
            pgn_data = pgn_data.strip()
        # Else, read the data from the file
        else:
            # Reading the PGN Data from the file
            with open(pgn_file.name, "r") as f:
                pgn_data = f.read().strip()
        # Create a PGN String Reader
        pgn = StringIO(pgn_data)
        # Read the PGN Data
        game = chess.pgn.read_game(pgn)
        # Get the details of the match
        headers = game.headers
        # Expander to see the details of the match
        with st.expander("Match Details"):
            st.write(headers)
        # Create a Chess Board
        board = chess.Board()
        # Get the moves of the match
        moves = list(game.mainline_moves())
        current_move = 0

        # Two buttons in a row to go through the moves of the match
        col1, col2 = st.columns(2)
        
        # Function to update the board
        def update_board(move_number):
            board = chess.Board()
            for move in moves[:move_number]:
                board.push(move)
            return board

        # Button to go to the previous move
        if col1.button("Previous Move"):
            # If the move is not the first move, go to the previous move
            if current_move > 0:
                current_move -= 1
                # Update the board and redraw it
                board = update_board(current_move)
        
        # Button to go to the next move
        if col2.button("Next Move"):
            # If the move is not the last move, go to the next move
            if current_move < len(moves):
                current_move += 1
                # Update the board and redraw it
                board = update_board(current_move)
        
        # Show the board as a picture
        board_svg = chess.svg.board(board=board, size=400)
        
        # Display the board as a picture
        st.image(board_svg, use_column_width="auto")