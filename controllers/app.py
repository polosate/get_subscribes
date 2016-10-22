from flask import Flask
import os.path
# import db_methods

BASE_DIR = '{}/../'.format(os.path.dirname(os.path.abspath(__file__)))
template_folder= os.path.join(BASE_DIR, 'templates')

app = Flask(__name__, template_folder=template_folder)

# app.db_sessions