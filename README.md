# Flask Smart Frame

Set a custom background video, view the weather and stock prices.

![flask frame](https://i.imgur.com/mXVg5NMl.jpg)

## Table of Contents
- [Background](#background)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Configuration](#configuration)
- [How it works](#how)
- [Hosting](#hosting)

## Background
For some time I wanted a "smart-monitor" application &mdash; a program that would show me the weather, stock prices, etc., and would feature a dynamic background, such as a Youtube video. This program would run on a raspberrypi and be displayed on a PC monitor.

Initially, I modified the popular [Smart Mirror application](https://github.com/HackerShackOfficial/Smart-Mirror) for these purposes. Though the application worked fairly well, designing the interface with Python's Tkinter was less than fun. Given my limited experience with Tkinter, having a background video at this point was not an option so I opted for a changing background image, which was achieved using Python's `os` library to randomly shuffle through pictures in a directory named `/images`. 

The app worked fairly well, though I was desperately missing my bread and butter of HTML, CSS, and JavaScript. The issue was that I didn't feel like configuring Node on a raspberrypi &mdash; I wanted the application to be in Python.

It wasn't until I started tooling around with Flask that I found my solution, and thus the creation of the `flask-smart-frame`.

## Getting started

### Prerequisites
- [Flask](http://flask.pocoo.org/docs/1.0/)
- [Sendgrid API key](https://sendgrid.com/)
- [Darsky API key](https://darksky.net/dev)

### Configuration

Here is a look at the configuration file for this application:

```python
class Config(object):
    ADMIN = os.environ.get('ADMIN') or 'davecrands@gmail.com'
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'secret-secrets-are-no-fun'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SENDGRID_API_KEY = os.environ.get('SENDGRID_API_KEY') or 'get-your-own'
    WEATHER_API_KEY = os.environ.get('WEATHER_API_KEY') or 'nice-try'
    LONGITUDE = os.environ.get('LONGITUDE') or 0.0
    LATITUDE = os.environ.get('LATITUDE') or 0.0
    YT_EMBED = os.environ.get('YT_EMBED') or 'XEfDYMngJeE
```

```
C:\flask-smart-frame>: set WEATHER_API_KEY=<api_key>
C:\flask-smart-frame>: set SENDGRID_API_KEY=<api_key>
C:\flask-smart-frame>: set =<api_key>
```

Set your latitude and longitude.
```
C:\flask-smart-frame>:set LONGITUDE=<lon>
C:\flask-smart-frame>:set LATITUDE=<lat>
```

Of course, you must configure `FLASK_APP`

```
C:\flask-smart-frame>:set FLASK_APP=run.py
```

### Set-up

Here is how I use this application:

1. It is served on a Raspberrypi connected to a PC monitor.
2. The web page is displayed full-screen in the Chromium browser.
3. `cronjob` and `vcgencmd` automate turning the display on/off according to my schedule
4. Hit refresh (F5) to update info. (this is to be automated)

## To Do
- Add user model
  - stock list
  - location (lat, lon)
  - YT embeds