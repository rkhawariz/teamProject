import os
from os.path import join, dirname
from dotenv import load_dotenv

from pymongo import MongoClient
import jwt
from datetime import datetime, timedelta
import hashlib
from flask import Flask, render_template, jsonify, request, redirect, url_for
from werkzeug.utils import secure_filename

app = Flask(__name__)

app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['UPLOAD_FOLDER'] = './static/profile_pics'

SECRET_KEY = 'MERZY'

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

MONGODB_URI = os.environ.get("MONGODB_URI")
DB_NAME =  os.environ.get("DB_NAME")

# client = MongoClient(MONGODB_URI)
# db = client[DB_NAME]

TOKEN_KEY = 'mytoken'

@app.route('/', methods= ['GET'])
def home():
  user_info = {
    'name': "Cindi Widiawati"
  }
  logged_in = True
  is_admin = False
  return render_template('index.html', user_info=user_info, logged_in=logged_in, is_admin=is_admin)

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/sign-up', methods=['GET', 'POST'])
def register():
    return render_template('register.html')
  
@app.route('/destinasi', methods=['GET'])
def destinations():
    return render_template('destinations.html')

@app.route('/detail_destinasi/<title>', methods=['GET'])
def detail_destinasi(title):
  user_info = {
    'name': "Rifqi Khawarij"
  }
  destinasi_info = {
    'namaDestinasi': "Yogyakarta",
    'namaAttr1': "Malioboro",
    'namaAttr2': "Candi Prambanan",
    'namaAttr3': "Pantai Parangtritis",
    'hargaTiketAttr1': 25000,
    'hargaTiketAttr2': 70000,
    'hargaTiketAttr3': 50000,
  }
  logged_in = True
  is_admin = False
  return render_template('detail_destinasi.html', user_info=user_info, destinasi_info=destinasi_info, logged_in=logged_in, is_admin=is_admin)
  
@app.route('/about', methods=['GET'])
def about():
  return render_template('about.html')
  
@app.route('/cek_pesanan')
def cek_pesanan():
  user_info = {
    'name': "Cindi Widiawati"
  }
  logged_in = True
  is_admin = False
  return render_template('cek_pesanan.html', user_info=user_info, logged_in=logged_in, is_admin=is_admin)

@app.route('/beranda_admin')
def beranda_admin():
  return render_template('beranda_admin.html')

@app.route('/manajemen_destinasi')
def manajemen_destinasi():
  return render_template('manajemen_destinasi.html')

@app.route('/manajemen_tiket')
def manajemen_tiket():
  return render_template('manajemen_tiket.html')

@app.route('/ulasan_rekomendasi')
def ulasan_rekomendasi():
  return render_template('ulasan_dan_rekom.html')

@app.route('/manajemen_user')
def manajemen_user():
  return render_template('manajemen_user.html')

@app.route('/profile_admin')
def profile_admin():
  return render_template('profile_Admin.html')

if __name__ == '__main__':
    app.run('0.0.0.0', port = 5000, debug = True)