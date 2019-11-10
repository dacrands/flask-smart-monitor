import requests
from flask import render_template, flash, redirect, url_for, request, jsonify
from flask_login import current_user, login_required
from werkzeug.urls import url_parse

from app import app, db

from app.models import User, Stock, Todo, Embed
from app.email import auth_email, reset_email
from app.forms import TodoForm, StockForm, EmbedForm, LocationForm


def getApiJson(apiUrl):
    """Return json from API request or empty dict"""
    apiReq = requests.get(apiUrl)
    if apiReq.status_code != 200:
        return {}
    return apiReq.json()


@app.route('/')
@app.route('/index')
@login_required
def index():
    """Return the index view with current_user's data"""
    todos = current_user.todos.all()
    userStocks = current_user.stocks.all()
    stockList = [stock.symbol for stock in userStocks]
    stockStr = ','.join(stockList).rstrip(',')

    userEmbeds = current_user.embeds.all()
    embedList = [(embed.embed, embed.name) for embed in userEmbeds]

    weatherUrl = "https://api.darksky.net/forecast/{0}/{1},{2}".format(
        app.config['WEATHER_API_KEY'],
        current_user.latitude,
        current_user.longitude)
    stocksUrl = "https://cloud.iexapis.com/v1/stock/market/batch?types=quote&symbols={0}&token={1}".format(
        stockStr, app.config['STOCKS_API_KEY'])

    weatherJson = getApiJson(weatherUrl)
    stocksJson = getApiJson(stocksUrl)

    return render_template('index.html',
                           todos=todos,
                           embeds=embedList,
                           weatherData=weatherJson,
                           stocksData=stocksJson)


@app.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    """Return CRUD view for User data"""
    (lat, lon) = (current_user.latitude, current_user.longitude)

    userStocks = current_user.stocks.all()
    stockList = [stock.symbol for stock in userStocks]

    userTodos = current_user.todos.all()
    todoList = [(todo.id, todo.todo) for todo in userTodos]

    userEmbeds = current_user.embeds.all()
    embedList = [(embed.embed, embed.name) for embed in userEmbeds]

    # TODO move all forms to top
    locationForm = LocationForm()
    # TODO move `if` blocks to a func
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


# TODO Use DELETE instead of POST
@app.route('/settings/<stock>', methods=['GET', 'POST'])
@login_required
def removeStock(stock):
    """Remove a User's Stock if it exists"""
    userStocks = current_user.stocks.all()
    # TODO Rename _stock
    for _stock in userStocks:
        if _stock.symbol == stock:
            db.session.delete(_stock)
            db.session.commit()
            flash('Removed stock!')
            return redirect('/settings')
    flash('Stock not found')
    return redirect('/settings')

# TODO Use DELETE instead of POST
@app.route('/settings/todo/<todo_id>', methods=['GET', 'POST'])
@login_required
def removeTodo(todo_id):
    """Remove a User's Todo if it exists"""
    userTodos = current_user.todos.all()
    for todo in userTodos:
        if todo.id == int(todo_id):
            db.session.delete(todo)
            db.session.commit()
            flash('Removed Todo!')
            return redirect('/settings')
    flash('Todo not found!')
    return redirect('/settings')

# TODO Use DELETE instead of POST
@app.route('/settings/embed/<embed_code>', methods=['GET', 'POST'])
@login_required
def removeEmbed(embed_code):
    """Remove a User's Embed if it exists"""
    userEmbeds = current_user.embeds.all()
    for embed in userEmbeds:
        if embed.embed == embed_code:
            db.session.delete(embed)
            db.session.commit()
            flash('Removed embed!')
            return redirect('/settings')
    flash('Embed not found!')
    return redirect('/settings')


@app.route('/about')
def about():
    return render_template('about.html')
