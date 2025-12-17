from flask import Flask, render_template, request, redirect, url_for, session, jsonify

from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from database import Database

from dotenv import load_dotenv
import os, re

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')
database = Database()
current_channel = 0

@app.route('/')
def home():
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    
    channels = database.get_channels()
    channel_names = [channel.name for channel in channels]
    
    if get_current_channel() == 0 and len(channels) > 0:
        set_current_channel(channels[0].id)
    
    messages = database.get_messages(current_channel)

    return render_template('index.html', channels=channels, messages=messages)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        password = request.form['password']
        if password == os.getenv('PASSWORD'):
            session['logged_in'] = True
            return redirect(url_for('home'))
        else:
            return "Incorrect password", 403

    return render_template('login.html')

@app.route('/channel_clicked', methods=['POST'])
def channel_clicked():
    channel_id = request.get_json().get('id')
    set_current_channel(channel_id)
    return jsonify({'status': 'success', 'id': channel_id})

@app.route('/create_channel', methods=['POST'])
def channel_created():
    channel_name = request.get_json().get('name')
    database.create_channel(channel_name)
    return jsonify({'status': 'success', 'name': channel_name})

@app.route('/delete_channel', methods=['POST'])
def channel_deleted():
    channel_id = request.get_json().get('id')
    database.delete_channel(channel_id)
    return jsonify({'status': 'success', 'name': channel_id})

@app.route('/create_message', methods=['POST'])
def create_message():
    message = request.get_json().get('message')
    database.create_message(get_current_channel(), message)
    return jsonify({'status': 'success', 'message': message})

@app.template_filter()
def linkify(text):
    # Regex to find URLs
    url_pattern = r'(https?://[^\s]+)'
    return re.sub(url_pattern, r'<a href="\1" target="_blank" rel="noopener noreferrer" style="color: #007BFF;">\1</a>', text)

def get_current_channel():
    global current_channel
    return current_channel

def set_current_channel(channel_id):
    global current_channel
    current_channel = channel_id

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6767, debug=True)