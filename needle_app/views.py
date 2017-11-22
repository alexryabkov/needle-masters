from datetime import datetime
from email import header
from flask import render_template, jsonify, url_for, redirect, request
from flask_mail import Mail
from needle_app import app
from needle_app.config import db
from needle_app.models import VisitStats, Image, Category
from needle_app.forms import ContactForm

header.MAXLINELEN = 64
IMAGES_PER_PAGE = 6


@app.route('/')
def index():
    # Need to think how to track/store unique remote addresses
    today_date = datetime.now().date()
    stat_rec = db.session.query(VisitStats).filter_by(date=today_date).first()
    if stat_rec:
        stat_rec.visits += 1
    else:
        db.session.add(VisitStats(date=today_date, visits=1))
    db.session.commit()
    return render_template('index.html.j2',
                           form=ContactForm(),
                           msg_sent=request.args.get('msg_sent', False))


def paginate_data(category, page):
    return db.session.query(Image).with_parent(category).paginate(
        page=page, per_page=IMAGES_PER_PAGE)


@app.route('/<category>/<int:page>')
def gallery_pagination(category, page):
    categ_data = db.session.query(Category).filter_by(name_en=category).first()
    return jsonify([image_data.to_json()
                    for image_data in paginate_data(categ_data, page).items])


@app.route('/gallery')
def gallery():
    pages_per_category = {}
    category_names = {}
    for category in db.session.query(Category).all():
        pages_per_category[category.name_en] = paginate_data(category, 1).pages
        category_names[category.name_en] = category.name_ru
    return render_template('gallery.html.j2',
                           categories=category_names,
                           pages_per_category=pages_per_category,
                           images_per_page=IMAGES_PER_PAGE)


@app.route('/sendemail', methods=['POST'])
def send_email():
    Mail(app).send_message(
        'Cообщение от пользователя ' + request.form['name'],
        recipients=app.config['MAIL_TO'],
        body='Cообщение от пользователя "{name}" <{email_addr}>\n\n{message}'
        .format(
            name=request.form['name'],
            email_addr=request.form['email_addr'],
            message=request.form['message']),
        sender=('Админ Штучки с иголочки', app.config['MAIL_USERNAME']))
    return redirect(url_for('index',
                            _anchor='contact-us',
                            msg_sent=True))
