from flask import Flask, render_template, request, redirect, session, url_for, flash
from pymongo import MongoClient, errors
from datetime import datetime, timedelta
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash, check_password_hash
from os import environ
import os
import logging
from bson import ObjectId

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY')
load_dotenv()

SECRET_KEY = environ.get('SECRET_KEY')
DB_USERNAME = environ.get('DB_USERNAME')
DB_PASSWORD = environ.get('DB_PASSWORD')
DB_HOST = environ.get('DB_HOST')
DB_DATABASE = environ.get('DB_DATABASE')
DB_PORT= environ.get('DB_PORT', 27017)

MONGODB_URI = f"mongodb://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/?authSource={DB_DATABASE}"

app.logger.info('Connecting to MongoDB...')
app.logger.info(f'MONGODB_URI: {MONGODB_URI}')
print(MONGODB_URI)
client = MongoClient(MONGODB_URI)
db = client[DB_DATABASE]
events_collection = db.events
users_collection = db.users

# Function to get current week dates
def get_week_dates():
    today = datetime.today()
    start_of_week = today - timedelta(days=today.weekday())
    return [(start_of_week + timedelta(days=i)).strftime("%A, %d %B %Y") for i in range(7)]

@app.route('/')
def index():
    week_dates = get_week_dates()
    return render_template('index.html', week_dates=week_dates)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username and password:
            # Authenticate user
            user = users_collection.find_one({'username': username})
            if user and check_password_hash(user['password'], password):
                session['username'] = username
                return redirect(url_for('open_day'))  # Redirect to the calendar page
            else:
                error = 'Invalid username or password'
                return render_template('login.html', error=error)
        else:
            error = 'Please enter both username and password'
            return render_template('login.html', error=error)

    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username and password:
            # Check if the username already exists
            if users_collection.find_one({'username': username}):
                error = 'Username already exists'
                return render_template('signup.html', error=error)

            # Hash the password and insert new user into the database
            hashed_password = generate_password_hash(password)
            try:
                users_collection.insert_one({'username': username, 'password': hashed_password})
                return redirect(url_for('login'))
            except Exception as e:
                app.logger.error(f"Error inserting new user: {e}")
                error = 'Error signing up, please try again later.'
                return render_template('signup.html', error=error)

        else:
            error = 'Please enter both username and password'
            return render_template('signup.html', error=error)

    return render_template('signup.html')

@app.route('/day/<day>', methods=['GET', 'POST'])
def day(day):
    if request.method == 'POST':
        hour = request.form.get('hour')
        text = request.form.get('text')
        
        # Check if the form is for adding an event
        if hour and text:
            try:
                events_collection.insert_one({'day': day, 'hour': hour, 'text': text})
                app.logger.debug(f"Inserted event for {day}: {hour} - {text}")  # Debugging statement
            except Exception as e:
                app.logger.error(f"Error inserting event: {e}")  # Debugging statement

        # Check if the form is for deleting an event
        elif 'delete_event' in request.form:
            event_id = request.form.get('delete_event')
            try:
                events_collection.delete_one({'_id': ObjectId(event_id)})
                app.logger.debug(f"Deleted event with ID {event_id}")  # Debugging statement
            except Exception as e:
                app.logger.error(f"Error deleting event: {e}")  # Debugging statement

        return redirect(url_for('day', day=day))    
    
    # Fetch events from the database for the current day
    try:
        events = list(events_collection.find({'day': day}))
        app.logger.debug(f"Fetched events for {day}: {events}")  # Debugging statement
    except Exception as e:
        app.logger.error(f"Error fetching events: {e}")  # Debugging statement
        events = []
    
    return render_template('day.html', day=day, events=events)

@app.route('/upload_picture/<day>', methods=['POST'])
def upload_picture(day):
    if 'picture' in request.files:
        picture = request.files['picture']
        picture_path = f'static/pictures/{day}.jpg'
        os.makedirs(os.path.dirname(picture_path), exist_ok=True)
        picture.save(picture_path)
        
        # Update or insert picture link into events_collection
        try:
            events_collection.update_one({'day': day}, {'$set': {'picture_path': picture_path}}, upsert=True)
        except Exception as e:
            app.logger.error(f"Error updating picture path: {e}")
    
    return redirect(url_for('day', day=day))

@app.route('/add_song/<day>', methods=['POST'])
def add_song(day):
    song_link = request.form.get('song_link')
    if song_link:
        events_collection.update_one({'day': day}, {'$set': {'song_link': song_link}}, upsert=True)
    return redirect(url_for('day', day=day))

@app.route('/cal', methods=['GET', 'POST'])
def open_day():
    week_dates = get_week_dates()
    return render_template('calendar.html', week_dates=week_dates)

if __name__ == '__main__':
    debug=True
    app.run(host='0.0.0.0', port=5000)
