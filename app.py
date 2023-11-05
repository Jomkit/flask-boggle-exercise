from boggle import Boggle
from flask import Flask, session

app = Flask(__name__)
app.config["SECRET_KEY"] = "SECRET1KEY2!"

boggle_game = Boggle()
