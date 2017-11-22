from flask_sqlalchemy import SQLAlchemy
from needle_app import app
import os

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(
    app.root_path, 'site_data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = \
    b'x\xd9"\x84\xbe\tB}J\xa6DZx\xf6\xf9\x89\x08\xb5P+{\x03\xad\xdf'
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config['MAIL_TO'] = ['e.filatova18@mail.ru']
# app.config['MAIL_TO'] = ['ramnn@mail.ru']
app.config['MAIL_SERVER'] = 'smtp.mail.ru'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'adm.shtuchki@mail.ru'
app.config['MAIL_PASSWORD'] = '123QWEasd!!!'

db = SQLAlchemy(app)
IMAGES_RELATIVE_PATH = 'images/'
IMAGES_BASE_PATH = os.path.join(app.static_folder, IMAGES_RELATIVE_PATH)
