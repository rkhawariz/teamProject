import os
from os.path import join, dirname
from dotenv import load_dotenv

from pymongo import MongoClient
import jwt
from datetime import datetime, timedelta
import hashlib
from flask import Flask, render_template, jsonify, request, redirect, url_for
from werkzeug.utils import secure_filename
from bson import ObjectId

app = Flask(__name__)

app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['UPLOAD_FOLDER'] = './static/profile_pics'

SECRET_KEY = 'MERZY'

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

MONGODB_URI = os.environ.get("MONGODB_URI")
DB_NAME =  os.environ.get("DB_NAME")

client = MongoClient(MONGODB_URI)
db = client[DB_NAME]

TOKEN_KEY = 'mytoken'

@app.route('/', methods= ['GET'])
def home():
  token_receive = request.cookies.get(TOKEN_KEY)
  try:
      payload =jwt.decode(
          token_receive,
          SECRET_KEY,
          algorithms=['HS256']
      )
      user_info = db.user.find_one({"email": payload["id"]})
      is_admin = user_info.get("role") == "admin"
      logged_in = True
      print(user_info)
      return render_template('index.html', user_info=user_info, logged_in=logged_in, is_admin=is_admin)
  except jwt.ExpiredSignatureError:
      msg = 'Your token has expired'
  except jwt.exceptions.DecodeError:
      msg = 'There was a problem logging you in'
  return render_template('index.html', msg=msg)

@app.route('/login')
def login():
  return render_template('login.html')

@app.route('/login_user', methods=['POST'])
def login_user():
    if request.method == 'POST':
        data = request.json
        email = data.get('email')
        password = data.get('password')
        pw_hash = hashlib.sha256(password.encode("utf-8")).hexdigest()
        
        result = db.user.find_one(
          {
           'email': email,
           'password': pw_hash
           }
        )
        if result:
            payload = {
                "id": email,
                "exp": datetime.utcnow() + timedelta(seconds=60 * 60 * 48)
            }
            token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
        return jsonify(
            {
                "success": True,
                'message': 'Login successful!',
                "token": token
            }
        )
    else:
      return jsonify({'success': False, 'message': 'Invalid email or password'}), 401
          
@app.route('/sign-up', methods=['GET'])
def get_register():
  return render_template('register.html')

@app.route('/sign-up', methods=['POST'])
def register():
    if request.method == 'POST':
        try:
            # Mengambil data dari permintaan POST
            data = request.json
            nama = data['nama']
            email = data['email']
            password = data['password']
            confirm_password = data['confirm_password']
            password_hash = hashlib.sha256(password.encode('utf-8')).hexdigest()

            # Memastikan password dan konfirmasi password sesuai
            if password == confirm_password:
                user_count = db.user.count_documents({})
                user_id = user_count + 1

                user_data = {
                    'id': user_id,
                    'nama': nama,
                    'email': email,
                    'password': password_hash,
                    'role': 'user',
                    'foto_profile': '',
                    'tanggal_register': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }

                # Insert user_data ke koleksi 'user'
                db.user.insert_one(user_data)

                return jsonify({'status': 'Success', 'message': 'Account created successfully'})
            else:
                return jsonify({'status': 'Error', 'message': 'Password and confirm password do not match'})
        except Exception as e:
            return jsonify({'status': 'Error', 'message': str(e)})
    return render_template('register.html')
  
@app.route('/destinasi', methods=['GET'])
def destinations():
  token_receive = request.cookies.get(TOKEN_KEY)
  try:
      payload =jwt.decode(
          token_receive,
          SECRET_KEY,
          algorithms=['HS256']
      )
      user_info = db.user.find_one({"email": payload["id"]})
      is_admin = user_info.get("role") == "admin"
      logged_in = True
      print(user_info)
      return render_template('destinations.html', user_info=user_info, logged_in=logged_in, is_admin=is_admin)
  except jwt.ExpiredSignatureError:
      msg = 'Your token has expired'
  except jwt.exceptions.DecodeError:
      msg = 'There was a problem logging you in'
  return render_template('destinations.html', msg=msg)

@app.route('/add_destinasi', methods=['POST'])
def add_destinasi():
    data = request.form
    
    nama_destinasi = data['namaDestinasi']
    card_destinasi = request.files['gambarCardDestinasi']
    extension_card = card_destinasi.filename.split('.')[-1]
    file_name_card = f'static/card/gambarCard-{nama_destinasi}.{extension_card}'
    card_destinasi.save(file_name_card)
  
    judul_attraction1 = data['judulAttraction1']
    subtitle_attraction1 = data['subtitleAttraction1']
    harga_attraction1 = int(data['hargaAttraction1'])
    gambar_attraction1 = request.files['gambarAttraction1']
    deskripsi_attraction1 = data['deskripsiAttraction1']
    extension_attr1 = gambar_attraction1.filename.split('.')[-1]
    file_name_attr1 = f'static/attraction/gambar-{judul_attraction1}.{extension_attr1}'
    gambar_attraction1.save(file_name_attr1)
    
    judul_attraction2 = data['judulAttraction2']
    subtitle_attraction2 = data['subtitleAttraction2']
    harga_attraction2 = int(data['hargaAttraction2'])
    gambar_attraction2 = request.files['gambarAttraction2']
    deskripsi_attraction2 = data['deskripsiAttraction2']
    extension_attr2 = gambar_attraction2.filename.split('.')[-1]
    file_name_attr2 = f'static/attraction/gambar-{judul_attraction2}.{extension_attr2}'
    gambar_attraction2.save(file_name_attr2)
    
    judul_attraction3 = data['judulAttraction3']
    subtitle_attraction3 = data['subtitleAttraction3']
    harga_attraction3 = int(data['hargaAttraction3'])
    gambar_attraction3 = request.files['gambarAttraction3']
    deskripsi_attraction3 = data['deskripsiAttraction3']
    extension_attr3 = gambar_attraction3.filename.split('.')[-1]
    file_name_attr3 = f'static/attraction/gambar-{judul_attraction3}.{extension_attr3}'
    gambar_attraction3.save(file_name_attr3)
    
    quotes = data['quotes']
    
    gambar_artikel = request.files['gambarArtikel']
    extension_artikel = gambar_artikel.filename.split('.')[-1]
    file_name_artikel = f'static/artikel/gambar-{nama_destinasi}.{extension_artikel}'
    gambar_artikel.save(file_name_artikel)
    deskripsi_artikel = data['deskripsiArtikel']

    destinasi_data = {
        'nama_destinasi': nama_destinasi,
        'card_destinasi': file_name_card,
        'attractions' : {
          'attraction1': {
            'judul': judul_attraction1,
            'subtitle': subtitle_attraction1,
            'harga': harga_attraction1,
            'gambar': file_name_attr1,
            'deskripsi_attraction1': deskripsi_attraction1
          },
          'attraction2': {
            'judul': judul_attraction2,
            'subtitle': subtitle_attraction2,
            'harga': harga_attraction2,
            'gambar': file_name_attr2,
            'deskripsi_attraction2': deskripsi_attraction2
          },
          'attraction3': {
            'judul': judul_attraction3,
            'subtitle': subtitle_attraction3,
            'harga': harga_attraction3,
            'gambar': file_name_attr3,
            'deskripsi_attraction3': deskripsi_attraction3
          }
        },
        'quotes': quotes,
        'gambar_artikel': file_name_artikel,
        'deskripsi_artikel': deskripsi_artikel,
        
        'tanggal_tambah': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    db.destinasi.insert_one(destinasi_data)
    return render_template('manajemen_destinasi.html')
      
@app.route('/manajemen_destinasi')
def manajemen_destinasi():
  token_receive = request.cookies.get(TOKEN_KEY)
  try:
      payload =jwt.decode(
          token_receive,
          SECRET_KEY,
          algorithms=['HS256']
      )
      user_info = db.user.find_one({"email": payload["id"]})
      is_admin = user_info.get("role") == "admin"
      logged_in = True
      if is_admin:
        return render_template('manajemen_destinasi.html', user_info=user_info, logged_in=logged_in, is_admin=is_admin)
      else:
        return render_template('login.html')
  except jwt.ExpiredSignatureError:
      msg = 'Your token has expired'
  except jwt.exceptions.DecodeError:
      msg = 'There was a problem logging you in'
  return render_template('login.html', msg=msg)

@app.route('/listdestinasi', methods=['GET'])
def get_destinasi():
  destinasi = db.destinasi.find()
  destinasi_list = []
  for destinasi_info in destinasi:
      destinasi_list.append({
          'id': str(destinasi_info['_id']),
          'name': destinasi_info['name'],
          'description': destinasi_info['description'],
          'image_wisata' : destinasi_info['image_wisata'],
          'total_tickets': destinasi_info['total_tickets']
      })
  return jsonify(destinasi_list), 200

@app.route('/detail_destinasi/<title>', methods=['GET'])
def detail_destinasi(title):
  user_info = {
    'name': "Rifqi Khawarij"
  }
  destinasi_info = {
    "nama_destinasi": "Banda Neira",
    "card_destinasi": "static/card/gambarCard-Yogyakarta.jpg",
    "attractions":{
     "attraction1":{
        "judul": "Pantai",
        "subtitle": "pantai di banda",
        "harga": {"$numberInt":"50000"},
        "gambar": "static/attraction/gambar-Pantai.png",
        "deskripsi_attraction1": "pantai ini ada di banda"
     },
     "attraction2":{
        "judul": "gunung",
        "subtitle": "gunung di banda",
        "harga": {"$numberInt":"35000"},
        "gambar": "static/attraction/gambar-gunung.png",
        "deskripsi_attraction2": "gunung ini ada di banda"
     },
     "attraction3":{
        "judul":"hutan",
        "subtitle":"hutan di banda",
        "harga":{"$numberInt":"1000"},
        "gambar":"static/attraction/gambar-hutan.png",
        "deskripsi_attraction3":"hutan ini ada di banda"
     }
    },
    "quotes":"the defitions of banda neira",
    "gambar_artikel":"static/artikel/gambar-Banda Neira.png",
    "deskripsi_artikel":"banda neira suatu tempat di banda",
    "tanggal_tambah":"2023-12-13 03:15:26"
  }
  
  logged_in = True
  is_admin = False
  return render_template('detail_destinasi.html', user_info=user_info, destinasi_info=destinasi_info, logged_in=logged_in, is_admin=is_admin)
  
@app.route('/pesantiket', methods=['POST'])
def pesantiket():
    namaAttraction = request.form['attractionGive']
    namaPemesan = request.form['namaPemesan']
    hargaTiket = request.form['hargaTiket']
    jumlahTiket = request.form['jumlahTiket']
    totalHargaTiket = request.form['totalHargaTiket']
    tanggal = request.form['tanggal']
    doc = {
      "namaAttraction" : namaAttraction,
      "namaPemesan" : namaPemesan,
      "hargaTiket" : hargaTiket,
      "jumlahTiket" : jumlahTiket,
      "totalHargaTiket" : totalHargaTiket,
      "tanggal" : tanggal,
      "status": "pending",
      "buktiPembayaran": "",
      "e-ticket": "",
    }
    db.tiket.insert_one(doc)
    return render_template('cek_pesanan.html')

@app.route('/about', methods=['GET'])
def about():
  token_receive = request.cookies.get(TOKEN_KEY)
  try:
      payload =jwt.decode(
          token_receive,
          SECRET_KEY,
          algorithms=['HS256']
      )
      user_info = db.user.find_one({"email": payload["id"]})
      is_admin = user_info.get("role") == "admin"
      logged_in = True
      print(user_info)
      return render_template('about.html', user_info=user_info, logged_in=logged_in, is_admin=is_admin)
  except jwt.ExpiredSignatureError:
      msg = 'Your token has expired'
  except jwt.exceptions.DecodeError:
      msg = 'There was a problem logging you in'
  return render_template('about.html', msg=msg)
  
@app.route('/cek_pesanan')
def cek_pesanan():
  user_info = {
    'name': "Cindi Widiawati"
  }
  logged_in = True
  is_admin = False
  return render_template('cek_pesanan.html', user_info=user_info, logged_in=logged_in, is_admin=is_admin)

@app.route('/beranda_admin', methods=['GET'])
def beranda_admin():
  token_receive = request.cookies.get(TOKEN_KEY)
  try:
      payload =jwt.decode(
          token_receive,
          SECRET_KEY,
          algorithms=['HS256']
      )
      user_info = db.user.find_one({"email": payload["id"]})
      is_admin = user_info.get("role") == "admin"
      logged_in = True
      if is_admin:
        return render_template('beranda_admin.html', user_info=user_info, logged_in=logged_in, is_admin=is_admin)
      else:
        return render_template('login.html')
  except jwt.ExpiredSignatureError:
      msg = 'Your token has expired'
  except jwt.exceptions.DecodeError:
      msg = 'There was a problem logging you in'
  return render_template('login.html', msg=msg)

@app.route('/manajemen_tiket', methods=['GET'])
def manajemen_tiket():
  token_receive = request.cookies.get(TOKEN_KEY)
  try:
      payload =jwt.decode(
          token_receive,
          SECRET_KEY,
          algorithms=['HS256']
      )
      user_info = db.user.find_one({"email": payload["id"]})
      is_admin = user_info.get("role") == "admin"
      logged_in = True
      if is_admin:
        return render_template('manajemen_tiket.html', user_info=user_info, logged_in=logged_in, is_admin=is_admin)
      else:
        return render_template('login.html')
  except jwt.ExpiredSignatureError:
      msg = 'Your token has expired'
  except jwt.exceptions.DecodeError:
      msg = 'There was a problem logging you in'
  return render_template('login.html', msg=msg)

@app.route('/ulasan_rekomendasi', methods=['GET'])
def ulasan_rekomendasi():
  token_receive = request.cookies.get(TOKEN_KEY)
  try:
      payload =jwt.decode(
          token_receive,
          SECRET_KEY,
          algorithms=['HS256']
      )
      user_info = db.user.find_one({"email": payload["id"]})
      is_admin = user_info.get("role") == "admin"
      logged_in = True
      if is_admin:
        return render_template('ulasan_dan_rekom.html', user_info=user_info, logged_in=logged_in, is_admin=is_admin)
      else:
        return render_template('login.html')
  except jwt.ExpiredSignatureError:
      msg = 'Your token has expired'
  except jwt.exceptions.DecodeError:
      msg = 'There was a problem logging you in'
  return render_template('login.html', msg=msg)

@app.route('/manajemen_user', methods=['GET'])
def manajemen_user():
  token_receive = request.cookies.get(TOKEN_KEY)
  try:
      payload =jwt.decode(
          token_receive,
          SECRET_KEY,
          algorithms=['HS256']
      )
      user_info = db.user.find_one({"email": payload["id"]})
      is_admin = user_info.get("role") == "admin"
      logged_in = True
      if is_admin:
        return render_template('manajemen_user.html', user_info=user_info, logged_in=logged_in, is_admin=is_admin)
      else:
        return render_template('login.html')
  except jwt.ExpiredSignatureError:
      msg = 'Your token has expired'
  except jwt.exceptions.DecodeError:
      msg = 'There was a problem logging you in'
  return render_template('login.html', msg=msg)

@app.route('/profile_admin', methods=['GET'])
def profile_admin():
  token_receive = request.cookies.get(TOKEN_KEY)
  try:
      payload =jwt.decode(
          token_receive,
          SECRET_KEY,
          algorithms=['HS256']
      )
      user_info = db.user.find_one({"email": payload["id"]})
      is_admin = user_info.get("role") == "admin"
      logged_in = True
      if is_admin:
        return render_template('profile_Admin.html', user_info=user_info, logged_in=logged_in, is_admin=is_admin)
      else:
        return render_template('login.html')
  except jwt.ExpiredSignatureError:
      msg = 'Your token has expired'
  except jwt.exceptions.DecodeError:
      msg = 'There was a problem logging you in'
  return render_template('login.html', msg=msg)

@app.route('/profile_User', methods=['GET'])
def profil_user():
  token_receive = request.cookies.get(TOKEN_KEY)
  try:
      payload =jwt.decode(
          token_receive,
          SECRET_KEY,
          algorithms=['HS256']
      )
      user_info = db.user.find_one({"email": payload["id"]})
      is_admin = user_info.get("role") == "admin"
      logged_in = True
      print(user_info)
      return render_template('profile_User.html', user_info=user_info, logged_in=logged_in, is_admin=is_admin)
  except jwt.ExpiredSignatureError:
      msg = 'Your token has expired'
  except jwt.exceptions.DecodeError:
      msg = 'There was a problem logging you in'
  return render_template('login.html', msg=msg)

if __name__ == '__main__':
    app.run('0.0.0.0', port = 5000, debug = True)