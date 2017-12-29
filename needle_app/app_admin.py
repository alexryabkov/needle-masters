from flask import redirect, url_for, flash
from flask_admin import Admin, AdminIndexView, expose
from flask_admin.base import BaseView
from flask_admin.contrib.sqla import ModelView
from flask_admin.form.upload import ImageUploadField, ImageUploadInput
from werkzeug.security import generate_password_hash, check_password_hash
from wtforms import validators
from wtforms.fields import StringField, PasswordField
from flask_wtf import FlaskForm
from needle_app import app
from needle_app.config import db, IMAGES_RELATIVE_PATH, IMAGES_BASE_PATH
from needle_app.models import AdminUser, VisitStats, Image, Category
import flask_login
import os
import string


# Define login and registration forms (for flask-login)
class LoginForm(FlaskForm):
    login = StringField(validators=[validators.InputRequired()])
    password = PasswordField(validators=[validators.InputRequired()])

    def validate_login(self, field):
        user = self.get_user()
        if user is None or not check_password_hash(user.password,
                                                   self.password.data):
            raise validators.ValidationError('Invalid login or password')

    def get_user(self):
        return db.session.query(AdminUser).filter_by(
            login=self.login.data).first()


# Define login and registration forms (for flask-login)
class ChangePwdForm(FlaskForm):
    new_password = PasswordField(
        validators=[validators.InputRequired()])
    confirm_password = PasswordField(
        validators=[validators.InputRequired()])

    def validate_new_password(self, field):
        if self.new_password.data != self.confirm_password.data:
            raise validators.ValidationError('Passwords should match!')


# Initialize flask-login
def init_login():
    login_manager = flask_login.LoginManager()
    login_manager.init_app(app)

    # Create user loader function
    @login_manager.user_loader
    def load_user(user_id):
        return db.session.query(AdminUser).get(user_id)


# Create customized index view class that handles login & registration
class MyAdminIndexView(AdminIndexView):

    def display_visitors_stats(self):
        stats = []
        for rec in db.session.query(VisitStats).order_by(
                VisitStats.date.desc()).limit(10).all()[::-1]:
            stats.append([rec.date.strftime('%b %d %Y'), rec.visits])
        return stats

    @expose('/')
    def index(self):
        if not flask_login.current_user.is_authenticated:
            return redirect(url_for('.login_view'))
        visits_dates, num_of_visits = map(list,
                                          zip(*self.display_visitors_stats()))
        return self.render('admin/index.html',
                           visits_dates=visits_dates,
                           num_of_visits=num_of_visits)

    @expose('/login/', methods=('GET', 'POST'))
    def login_view(self):
        # handle user login
        form = LoginForm()
        if form.validate_on_submit():
            user = form.get_user()
            flask_login.login_user(user)

        if flask_login.current_user.is_authenticated:
            return redirect(url_for('.index'))
        self._template_args['form'] = form
        visits_dates, num_of_visits = map(list,
                                          zip(*self.display_visitors_stats()))
        return self.render('admin/index.html',
                           visits_dates=visits_dates,
                           num_of_visits=num_of_visits)

    @expose('/logout/')
    def logout_view(self):
        flask_login.logout_user()
        return redirect(url_for('.index'))


# Create customized index view class that handles login & registration
class ChangeAdminPassword(BaseView):
    @expose('/', methods=('GET', 'POST'))
    def index(self):
        if not flask_login.current_user.is_authenticated:
            return redirect(url_for('admin.login_view'))

        form = ChangePwdForm()
        if form.validate_on_submit():
            db.session.query(AdminUser).filter_by(
                login=flask_login.current_user.login).update(
                {'password': generate_password_hash(form.new_password.data)})
            db.session.commit()
            flash('The password was updated successfully!')
        return self.render("admin/change_pwd.html", form=form)


class ImageFieldWidget(ImageUploadInput):
    data_template = (
        '<div class="image-thumbnail">'
        ' <img style="max-width: 200px; max-height: 200px;" %(image)s>'
        ' <input %(text)s>'
        '</div>'
        '<br>'
        '<input %(file)s>')


class ImageField(ImageUploadField):
    widget = ImageFieldWidget()


class ImageView(ModelView):

    def is_accessible(self):
        return flask_login.current_user.is_authenticated

    def after_model_delete(self, model):
        file_path = os.path.join(IMAGES_BASE_PATH, model.filename)
        fname, ext = os.path.splitext(model.filename)
        file_thumb_path = os.path.join(
            IMAGES_BASE_PATH, ''.join([fname, '_thumb', ext]))

        if os.path.exists(file_path):
            os.remove(file_path)
        if os.path.exists(file_thumb_path):
            os.remove(file_thumb_path)

    column_labels = dict(item_price='Item Price (RUB)')
    form_extra_fields = {
        'filename': ImageField('Image File',
                               base_path=IMAGES_BASE_PATH,
                               validators=[validators.DataRequired()],
                               url_relative_path=IMAGES_RELATIVE_PATH,
                               thumbnail_size=(200, 200, True))
    }
    form_rules = ('filename', 'item_name', 'item_price',
                  'category', 'description')


class CategoryView(ModelView):

    def on_model_change(self, form, model, is_created):
        error_text = '"Name En" field can contain only latin letters, digits, \
                       whitespaces, hyphens ( - ) and underscores ( _ )'
        allowed_chars = set(string.ascii_letters + string.digits +
                            ' ' + '-' + '_')
        if not set(model.name_en).issubset(allowed_chars):
            raise validators.ValidationError(error_text)
        model.name_en = model.name_en.replace(' ', '-')


init_login()
admin = Admin(app, name='Admin page',
              index_view=MyAdminIndexView(),
              base_template='admin/master_custom.html',
              template_mode='bootstrap3')
admin.add_view(ImageView(Image, db.session, 'Images'))
admin.add_view(CategoryView(Category, db.session, 'Categories'))
admin.add_view(ChangeAdminPassword())
