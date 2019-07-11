import requests
from flask import render_template, flash, redirect, url_for, request, jsonify
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.urls import url_parse

from app import app, db
from app.forms import TodoForm, StockForm, LoginForm, EmbedForm,\
    RegistrationForm, LocationForm,\
    ResetPasswordForm, NewPasswordForm, DeleteUserForm


from app.models import User, Stock, Todo, Embed
from app.email import auth_email, reset_email


"""
=========
INDEX
=========
"""
@app.route('/')
@app.route('/index')
@login_required
def index():
    todoForm = TodoForm()
    todos = current_user.todos.all()

    userStocks = current_user.stocks.all()
    stockList = [stock.symbol for stock in userStocks]

    userEmbeds = current_user.embeds.all()
    embedList = [(embed.embed, embed.name) for embed in userEmbeds]

    stockStr = ','.join(stockList).rstrip(',')

    STOCKS_URL = "https://api.iextrading.com/1.0/stock/market/batch?symbols={0}&types=quote,news,chart&range=1m&last=10".format(
        stockStr)

    WEATHER_URL = "https://api.darksky.net/forecast/{0}/{1},{2}".format(
        app.config['WEATHER_API_KEY'], current_user.latitude, current_user.longitude)

    weatherRes = requests.get(WEATHER_URL)

    if weatherRes.status_code != 200:
        weatherJson = False
    else:
        weatherJson = weatherRes.json()

    stocksRes = requests.get(STOCKS_URL)
    if stocksRes.status_code != 200:
        stocksJson = []
    else:
        stocksJson = stocksRes.json()

    return render_template('index.html',
                           todos=todos,
                           embeds=embedList,
                           todoForm=todoForm,
                           weatherData=weatherJson,
                           stocksData=stocksJson)


"""
=========
SETTINGS
=========
"""
@app.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    (lat, lon) = (current_user.latitude, current_user.longitude)

    userStocks = current_user.stocks.all()
    stockList = [stock.symbol for stock in userStocks]

    userTodos = current_user.todos.all()
    todoList = [(todo.id, todo.todo) for todo in userTodos]

    userEmbeds = current_user.embeds.all()
    embedList = [(embed.embed, embed.name) for embed in userEmbeds]

    locationForm = LocationForm()
    if locationForm.submitLoc.data and locationForm.validate_on_submit():
        current_user.set_location(locationForm.lat.data, locationForm.lon.data)
        db.session.commit()
        flash('Updated location.')
        return redirect('/settings')

    stockForm = StockForm()
    if stockForm.submitStock.data and stockForm.validate_on_submit():
        stock = Stock(symbol=stockForm.symbol.data, author=current_user)
        db.session.add(stock)
        db.session.commit()
        flash('Added stock!')
        return redirect('/settings')

    todoForm = TodoForm()
    if todoForm.submitTodo.data and todoForm.validate_on_submit():
        todo = Todo(todo=todoForm.todo.data, author=current_user)
        db.session.add(todo)
        db.session.commit()
        flash('Added todo!')
        return redirect('/settings')

    embedForm = EmbedForm()
    if embedForm.submitEmbed.data and embedForm.validate_on_submit():
        embed = Embed(embed=embedForm.embed.data,
                      name=embedForm.name.data,
                      author=current_user)
        db.session.add(embed)
        db.session.commit()
        flash('Added embed!')
        return redirect('/settings')

    return render_template('settings.html',
                           stocks=stockList,
                           stockForm=stockForm,
                           todoForm=todoForm,
                           todos=todoList,
                           embedForm=embedForm,
                           embeds=embedList,
                           locationForm=locationForm,
                           lat=lat,
                           lon=lon)


"""
=========
SETTINGS 
- edit
=========
"""
@app.route('/settings/<stock>', methods=['GET', 'POST'])
@login_required
def removeStock(stock):
    userStocks = current_user.stocks.all()
    for _stock in userStocks:
        if _stock.symbol == stock:
            db.session.delete(_stock)
            db.session.commit()
            flash('Removed stock!')
            return redirect('/settings')
    flash('Stock not found')
    return redirect('/settings')


@app.route('/settings/todo/<todo_id>', methods=['GET', 'POST'])
@login_required
def removeTodo(todo_id):
    userTodos = current_user.todos.all()
    for todo in userTodos:
        if todo.id == int(todo_id):
            db.session.delete(todo)
            db.session.commit()
            flash('Removed Todo!')
            return redirect('/settings')
    flash('Todo not found!')
    return redirect('/settings')


@app.route('/settings/embed/<embed_code>', methods=['GET', 'POST'])
@login_required
def removeEmbed(embed_code):
    userEmbeds = current_user.embeds.all()
    for embed in userEmbeds:
        if embed.embed == embed_code:
            db.session.delete(embed)
            db.session.commit()
            flash('Removed embed!')
            return redirect('/settings')
    flash('Embed not found!')
    return redirect('/settings')


"""
=========
ABOUT
=========
"""
@app.route('/about')
def about():
    return render_template('about.html')


"""
=========
REGISTER
=========
"""
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)

        # Initiliaze some cools videos!
        embed1 = Embed(embed='mFlrc16xjik',
                       name='Ocean stuff, whales, etc.',
                       author=user)

        embed2 = Embed(embed='Zk0W2UvyINM',
                       name='Relaxing nature',
                       author=user)

        db.session.add(embed1)
        db.session.add(embed2)
        db.session.commit()

        token = user.get_email_token()
        auth_email('welcome@flaskframe.com',
                   'Verify Your Account!',
                   user.email,
                   render_template('email/reg_email.html', token=token))
        flash('Thanks! We just sent an email confirmation. ')
        return redirect(url_for('login'))
    return render_template('auth/register.html', form=form)


"""
=========
LOGIN
=========
"""
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    token = request.args.get('token')
    if token:
        user_id = User.verify_email_token(token)
        if type(user_id) == None:
            flash('Something went wrong! Please try logging in.')
            return redirect(url_for('index'))
        user = User.query.get(user_id)
        user.set_verify(True)
        db.session.commit()
        login_user(user)
        return redirect(url_for('index'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        if not user.is_verified:
            flash('You need to verify your account')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('auth/login.html', form=form)


"""
=========
LOGOUT
=========
"""
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


"""
=========
DELETE USER
=========
"""
@app.route('/delete', methods=['GET', 'POST'])
@login_required
def delete_user():
    form = DeleteUserForm()
    if form.validate_on_submit():
        if current_user.check_password(form.password.data):
            user = User.query.filter_by(id=current_user.id).first()
            db.session.delete(user)
            db.session.commit()

            # You need to log out the user to remove the cookie,
            # This caused me a headache, not literally, but you understand.
            logout_user()
            flash('Account deleted.')
            return(redirect('/login'))
        flash('That password does not seem to match')
        return render_template('auth/delete_user.html', form=form)
    return render_template('auth/delete_user.html', form=form)


"""
=========
PASSWORD
NEW
=========
"""
@app.route('/new_password/<token>', methods=['GET', 'POST'])
def new_password(token):
    user_id = User.verify_email_token(token)
    if type(user_id) == None:
        flash('Something went wrong! Please submit another password reset request.')
        return redirect(url_for('index'))
    user = User.query.get(user_id)
    if not user:
        return redirect(url_for('index'))
    form = NewPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('auth/new_password.html', form=form)


"""
=========
PASSWORD
RESET
=========
"""
@app.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            token = user.get_email_token()
            reset_email('reset@flaskframe.com',
                        'Reset Password',
                        user.email,
                        render_template('email/reset_email.html', token=token))
            flash('Thanks! We just sent a reset link.')
            return redirect(url_for('login'))
        flash('Thanks! We just sent a reset link.')
        return redirect(url_for('login'))
    return render_template('auth/reset_password.html', form=form)
