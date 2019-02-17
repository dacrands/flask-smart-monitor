![flask frame](https://i.imgur.com/yTIpYmGl.jpg)

# ToViewIt

ToViewIt is a productivity application and a piece of art. More specifically, it is a to-do list application that has all sorts of extra features, intended to be used on either your desktop or laptop.


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
- MySQL database
- Docker containers
- Youtube IFrame API


## Table of Contents
- [Description](#description)
  - [Prerequisites](#prerequisites)
  - [Configuration](#configuration)
- [How it works](#how)
- [Hosting](#hosting)

<!-- ## Backgrounds

For some time I wanted a "smart-monitor" application &mdash; a program that would show me the weather, stock prices, etc., and would feature a dynamic background, such as a Youtube video. This program would run on a raspberrypi and be displayed on a PC monitor.

Initially, I modified the popular [Smart Mirror application](https://github.com/HackerShackOfficial/Smart-Mirror) for these purposes, and while the application worked fairly well, designing the interface with Python's Tkinter was less than fun. 

Given my limited experience with Tkinter, having a background video at this point was not an option so I opted for a changing background image, which was achieved using Python's `os` library to randomly shuffle through pictures in a directory named `/images`. 


The app worked fairly well, though I was desperately missing my bread and butter of HTML, CSS, and JavaScript. The issue was that I didn't feel like configuring Node on a raspberrypi &mdash; I wanted the application to be in Python.

It wasn't until I started tooling around with Flask that I found my solution, and thus the creation of the `flask-smart-frame`. -->

## Description
**ToViewIt** is a productivity application built using Flask. The application and the associated MySQL database are deployed from Docker containers hosted on DigitalOcean. The following instructions assume that you have familiarity with Flask and configuring Python environments, either using `pip` or `conda`. (If you're new to this, I wrote a [blog post](https://dacrands.github.io/10-7-18) that will get you started with your first Flask application.) Additionally, you will need to sign-up for two free APIs.

### Prerequisites
- [Flask](http://flask.pocoo.org/docs/1.0/)
- [Sendgrid API key](https://sendgrid.com/)
- [Darsky API key](https://darksky.net/dev)
- [Heroku](https://www.heroku.com/) (Optional)

### Configuration
The following instructions are for Windows users, Unix users will use `bin source activate` to activate their application's environment and `export` to set environment variables.

Activate your environment and install the necessary packages

```
C:\flask-smart-frame>: activate smart_frame_env 
(smart_frame_env) C:\flask-smart-frame>: pip install requirements.txt
```


Then set the following environmental variables. 


```
(smart_frame_env) C:\flask-smart-frame>:set FLASK_APP=run.py
(smart_frame_env) C:\flask-smart-frame>: set WEATHER_API_KEY=<api_key>
(smart_frame_env) C:\flask-smart-frame>: set SENDGRID_API_KEY=<api_key>
```

Last, initialize your database.
```
(smart_frame_env) C:\flask-smart-frame>: flask db init
```

## Hosting

The following instructions will get the application running on Heroku. 

If you didn't know what the `Procfile` does, it's instructions for Heroku on how to run an 
application. 

```
web: flask db upgrade; gunicorn run:app
```

I won't delve into the specifics, but generally:
-  `web` tells Heroku we are hosting a web application
- `flask db upgrade` upgrades our db
- `gunicorn run:app` starts our [gunicorn](https://gunicorn.org/) server and starts the app


### Download Heroku and deploy your first application

Heroku is free and easy to use. Here is the ["Getting Started on Heroku with Python" tutorial](https://devcenter.heroku.com/articles/getting-started-with-python). Heroku has excellent documentation, so please be sure to finish their tutorial before proceeding.

### Create a New App
You should know how to do this, but just as a refresher:

```
heroku create
```

Then push the repo...
```
git push heroku master
```

### Config Vars
Given that you finished the tutorial linked above, you learned about [config vars](https://devcenter.heroku.com/articles/getting-started-with-python#define-config-vars) and how to configure them. 

Set the following `config vars`:
- FLASK_APP=run.py
- SENDGRID_API_KEY=<YOUR_SENGRID_KEY>
- WEATHER_API_KEY=<YOUR_DARKSKY_KEY>

### Configure Postgresql
Last, configure your database.

```
 heroku addons:add heroku-postgresql:hobby-dev
```

And that should do it. If you run into any issues, such as with db migrations, you can always [start up a heroku console](https://devcenter.heroku.com/articles/getting-started-with-python#start-a-console) and run the flask shell.

```
heroku run flask shell
```

## Author

David Crandall
