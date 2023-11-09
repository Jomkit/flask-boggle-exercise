from boggle import Boggle
from flask import Flask, session, request,  render_template, jsonify, redirect
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config["SECRET_KEY"] = "SECRET1KEY2!"
debug = DebugToolbarExtension(app)
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

#Initialized variables
boggle_game = Boggle()

@app.route('/')
def play():
    return render_template('start-game.html')

@app.route('/set-board-size', methods=['post'])
def set_board_size():
    """Sets the board size, default 5"""
    board_size = request.form.get('board-size')
    if board_size == '':
        board_size = 5
    global boggle_game
    boggle_game = Boggle(int(board_size))
    return redirect('/home')

@app.route('/home')
def homepage():
    """Home Page Route"""
    board = boggle_game.make_board()
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
    board = session['board']
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

@app.route('/reset-stats')
def reset_statistics():
    """
    reset_statistics()
    Resets the values in the session for curr-hi-score and 
    num_played to zero, then redirects to home
    """
    session['curr-hi-score'] = 0
    session['num_played'] = 0
    return redirect('/')