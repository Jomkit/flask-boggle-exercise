from boggle import Boggle
from flask import Flask, session, request,  render_template, redirect
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config["SECRET_KEY"] = "SECRET1KEY2!"
debug = DebugToolbarExtension(app)

boggle_game = Boggle()
board = boggle_game.make_board()

@app.route('/')
def index():
    """Home Page Route"""
    session['board'] = board

    return render_template('home.html')
