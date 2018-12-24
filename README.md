# Flask Smart Frame

Flask Smart Frame is a productivity application and a piece of art. More specifically, it is a to-do list application that has all sorts of extra features, intended to be used on either your desktop or laptop.


![flask frame](https://i.imgur.com/yTIpYmGl.jpg)

### User Features

- **To Do List** 
    - Easily add/remove "to dos" that appear in a movable window
- **Stock Ticker** 
    - Easily add/remove stocks to appear in the scrolling ticker
- **Weather** 
    - Set your location and receive real-time weather information
- **YouTube Background Video** 
    - Save your favorite YouTube videos to appear as full-screen backgrounds. 

### Application Features
- User authentication and password resets using the SendGrid email client
- Bcrypt password encryption
- Postgresql database
- Heroku hosting
- Youtube IFrame API


## Table of Contents
<!-- - [Background](#background) -->
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Configuration](#configuration)
- [How it works](#how)
- [Hosting](#hosting)

## Backgrounds

For some time I wanted a "smart-monitor" application &mdash; a program that would show me the weather, stock prices, etc., and would feature a dynamic background, such as a Youtube video. This program would run on a raspberrypi and be displayed on a PC monitor.

Initially, I modified the popular [Smart Mirror application](https://github.com/HackerShackOfficial/Smart-Mirror) for these purposes, and while the application worked fairly well, designing the interface with Python's Tkinter was less than fun. Given my limited experience with Tkinter, having a background video at this point was not an option so I opted for a changing background image, which was achieved using Python's `os` library to randomly shuffle through pictures in a directory named `/images`. 

The app worked fairly well, though I was desperately missing my bread and butter of HTML, CSS, and JavaScript. The issue was that I didn't feel like configuring Node on a raspberrypi &mdash; I wanted the application to be in Python.

It wasn't until I started tooling around with Flask that I found my solution, and thus the creation of the `flask-smart-frame`.

## Getting started


### Prerequisites
- [Flask](http://flask.pocoo.org/docs/1.0/)
- [Sendgrid API key](https://sendgrid.com/)
- [Darsky API key](https://darksky.net/dev)

### Configuration

In order for your application to function, you will need to set the following environmental variables. The following instructions are for Windows users, Unix users will use `export`.


```
C:\flask-smart-frame>: set WEATHER_API_KEY=<api_key>
C:\flask-smart-frame>: set SENDGRID_API_KEY=<api_key>
C:\flask-smart-frame>: set =<api_key>
```

If you'd like to set a default weather location for all users, you can do so by setting the following environment variables &mdhash; this is a placeholder until users set their weather location.   
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