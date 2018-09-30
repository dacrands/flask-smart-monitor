import requests
from flask import render_template, flash, redirect, url_for, request, jsonify
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.urls import url_parse

from app import app, db
from app.forms import LoginForm, RegistrationForm
from app.models import User

stockList = ["f", "fb", "aapl", "vt", "siri", "amd", "fit", "tsla"]
stockStr = ','.join(stockList).rstrip(',')

WEATHER_URL = "https://api.darksky.net/forecast/{0}/{1},{2}".format(
    app.config['WEATHER_API_KEY'], app.config['LATITUDE'], app.config['LONGITUDE'])
STOCKS_URL = "https://api.iextrading.com/1.0/stock/market/batch?symbols={0}&types=quote,news,chart&range=1m&last=10".format(
    stockStr)


@app.route('/')
@app.route('/index')
@login_required
def index():
    weatherRes = requests.get(WEATHER_URL)
    weatherJson = weatherRes.json()

    stocksRes = requests.get(STOCKS_URL)
    stocksJson = stocksRes.json()

    return render_template('index.html', weatherData=weatherJson, stocksData=stocksJson, YTembed=app.config['YT_EMBED'])


@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            print("==============ASD===============")
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations! You are now registered!')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)