from boggle import Boggle
from flask import Flask, session, request,  render_template, jsonify
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config["SECRET_KEY"] = "SECRET1KEY2!"
debug = DebugToolbarExtension(app)

#For testing
app.config['TESTING'] = True
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

#Initialized variables
boggle_game = Boggle()
board = boggle_game.make_board()

@app.route('/')
def index():
    """Home Page Route"""
    session['board'] = board
    num_played = session.get('num_played', 0)
    session['num_played'] = num_played

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

@app.route('/store-statistics', methods=['post'])
def store_statistics():
    """ 
    store_statistics()
    Compares the score of the current game of
    boggle, if greater than stored hi-score then
    update hi-score. Also counts the number of times
    played
    """
    num_played = session.get('num_played', 0)
    session['num_played'] = num_played + 1

    res = request.get_json()
    score = res.get('score')
    session['curr-hi-score'] = session.get('curr-hi-score', 0)
    new_hi_score = session['curr-hi-score']

    if session['curr-hi-score'] < score:
        session['curr-hi-score'] = score
        new_hi_score = score
    
    return jsonify(new_hi_score)