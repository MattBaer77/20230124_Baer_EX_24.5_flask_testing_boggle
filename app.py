
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
    """Show homepage with button to start the game."""
    return render_template("home.html")

@app.route("/board")
def game_board():
    """Show gameboard when game starts."""

    boggle_board = boggle_game.make_board()
    session["board"] = boggle_board
    # print(boggle_board)

    return render_template("board.html", board=boggle_board)

@app.route("/check-word")
def check_word():
    """
        Handle request to check word.
        Accept a word
        Check if that word is in the reference dictionary
        Check if that word is on the board
        Return a JSON object containing {'result' : response}

    """

    word_to_check = request.args["word"]
    board = session["board"]
    # print(board)
    # print(word_to_check)

    response = boggle_game.check_valid_word(board, word_to_check)
    # print(response)
    
    # print("recieved check-word request")
    return jsonify({'result' : response})

    # test this to see if it breaks the app
    # return ({'result' : response})

@app.route("/post-score", methods=["POST"])
def post_score():
    """
    Handle post request
    Update number of plays
    Determine if score recieved is new high score
    Return response if score is new high score or not
    """

    print(request.json)
    # dir(request.json)

    score = request.json["score"]

    highscore = session.get("highscore", 0)
    number_plays = session.get("number_plays", 0)

    if_new_high_score = False

    if score > highscore:
        highscore = score

    session["number_plays"] = number_plays + 1
    session["highscore"] = highscore

    print(session["number_plays"])
    print(session["highscore"])

    return jsonify({"highScore": highscore})