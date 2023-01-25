
# Imports
from flask import Flask, request, render_template, redirect, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from boggle import Boggle

# Setup
app = Flask(__name__)
app.config["SECRET_KEY"] = "Nick_Cage"
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False
debug = DebugToolbarExtension(app)

# Instantiate Boggle Game
boggle_game = Boggle()    

@app.route("/")
def home_page():
    return render_template("home.html")

@app.route("/board")
def game_board():

    boggle_board = boggle_game.make_board()
    session["board"] = boggle_board
    print(boggle_board)

    return render_template("board.html", board=boggle_board)

@app.route("/check-word")
def check_word():

    word_to_check = request.args["word"]
    board = session["board"]
    print(board)
    print(word_to_check)

    response = boggle_game.check_valid_word(board, word_to_check)
    print(response)
    
    print("recieved check-word request")
    return jsonify({'result' : response})

    # test this to see if it breaks the app
    # return ({'result' : response})

