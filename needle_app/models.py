from werkzeug.security import generate_password_hash
from flask import url_for
from needle_app import app
from needle_app.config import IMAGES_RELATIVE_PATH, IMAGES_BASE_PATH, db
from datetime import datetime
from PIL import Image as Img
import os
import shutil


# Create user model
class AdminUser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(200))

    # Flask-Login integration
    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    # Required for administrative interface
    def __unicode__(self):
        return self.login


# Create visits statistics model
class VisitStats(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date)
    visits = db.Column(db.Integer)


# Create category model
class Category(db.Model):

    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    name_en = db.Column(db.String(200), nullable=False, unique=True)
    name_ru = db.Column(db.String(200), nullable=False, unique=True)

    def __repr__(self):
        '''
        Printable representation of an object
        '''
        return self.name_ru


# Create image model
class Image(db.Model):

    __tablename__ = 'images'

    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(100), nullable=False, unique=True)
    item_name = db.Column(db.String(100), nullable=False)
    item_price = db.Column(db.String(20), nullable=False)
    description = db.Column(db.String(300), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'),
                            nullable=False)
    category = db.relationship('Category',
                               backref=db.backref('items', lazy=True))

    def __repr__(self):
        '''
        Printable representation of an object
        '''
        return '<Image (%s, %s, %s, %s, %s)>' % (self.filename,
                                                 self.item_name,
                                                 self.item_price,
                                                 self.description,
                                                 self.category)

    def to_json(self):
        '''
        Convert data to JSON
        '''
        return dict(filepath=url_for(
            'static',
            filename=os.path.join(IMAGES_RELATIVE_PATH,
                                  self.filename)),
                    item_name=self.item_name,
                    item_price=self.item_price,
                    description=self.description)


# Command to inintialize the DB with default data.
# Please note: the operation cannot be undone so use with caution!
@app.cli.command('initdb')
def initdb_command():
    if input('THIS CAN\'T BE UNDONE: Drop the existing Images DB table and '
             'initialize it with the default data? (Y/N) ').lower() == 'y':

        default_categories = [('beadwork', 'Вышивка бисером'),
                              ('bead-weaving', 'Бисероплетение'),
                              ('cross-stitch', 'Вышивка крестом')]

        print('Deleting DB tables and all image files...')
        db.drop_all()
        for fn in os.listdir(IMAGES_BASE_PATH):
            fn_path = os.path.join(IMAGES_BASE_PATH, fn)
            if os.path.isfile(fn_path):
                os.remove(fn_path)

        print('DB initialization...')
        db.create_all()

        admin = AdminUser(
            login="admin", password=generate_password_hash("admin"))
        db.session.add(admin)

        print('Adding default data to DB...')
        db.session.add(VisitStats(date=datetime.now().date(), visits=1))
        for categ_name_en, categ_name_ru in default_categories:
            categ_record = Category(name_en=categ_name_en,
                                    name_ru=categ_name_ru)
            data_dir = os.path.join(app.static_folder,
                                    'default_data', categ_name_en)
            for file_name in os.listdir(data_dir):
                Image(filename=file_name, item_name='Имя изделия',
                      item_price='1000.00',
                      description='Описание изделия',
                      category=categ_record)

                file_path = os.path.join(data_dir, file_name)
                fname, ext = os.path.splitext(file_name)
                file_thumb_path = os.path.join(
                    IMAGES_BASE_PATH, ''.join([fname, '_thumb', ext]))

                shutil.copy(file_path, IMAGES_BASE_PATH)
                # Create file thumbnail
                im = Img.open(file_path)
                im.thumbnail((200, 200), Img.ANTIALIAS)
                im.save(file_thumb_path)

            db.session.add(categ_record)

        db.session.commit()
        print('Done!')
