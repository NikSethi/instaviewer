from flask import Flask, render_template
from instagram.client import InstagramAPI

app = Flask(__name__)
from app import views