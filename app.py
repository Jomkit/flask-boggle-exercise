from boggle import Boggle
from flask import Flask, session, request,  render_template, jsonify
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config["SECRET_KEY"] = "SECRET1KEY2!"
debug = DebugToolbarExtension(app)

#Initialized variables
boggle_game = Boggle()
board = boggle_game.make_board()

@app.route('/')
def index():
    """Home Page Route"""
    session['board'] = board

    return render_template('home.html')

@app.route('/check-word', methods=['post'])
def check_word():
    """
    Check word and return whether it is ok,
    not-on-board, or not-word
    """
    res = request.get_json()
    word = res.get('word')
    result = boggle_game.check_valid_word(board, word)

    return result