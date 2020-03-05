from flask_sqlalchemy import SQLAlchemy
from needle_app import app
import os

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(
    app.root_path, 'site_data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = ''
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config['MAIL_TO'] = ['test@mail.ru']
# app.config['MAIL_TO'] = ['ramnn@mail.ru']
app.config['MAIL_SERVER'] = 'smtp.mail.ru'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'mysuperadmin@mail.ru'
app.config['MAIL_PASSWORD'] = 'dummy!'

db = SQLAlchemy(app)
IMAGES_RELATIVE_PATH = 'images/'
IMAGES_BASE_PATH = os.path.join(app.static_folder, IMAGES_RELATIVE_PATH)
