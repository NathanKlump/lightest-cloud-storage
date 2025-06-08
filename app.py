from flask import Flask, render_template, request, jsonify

from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from database import Database

app = Flask(__name__)
database = Database()
current_channel = 0

@app.route('/')
def home():
    # database.create_new_channel("test channel")
    channels = database.get_channels()
    channel_names = [channel.name for channel in channels]
    
    if get_current_channel() is 0 and len(channels) is not 0:
        set_current_channel(channels[0].id)
    
    messages = database.get_messages(current_channel)

    return render_template('index.html', channels=channels, messages=messages)

@app.route('/channel_clicked', methods=['POST'])
def channel_clicked():
    channel_id = request.get_json().get('id')
    print(f"Channel clicked")
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
    print("trying to delete")
    database.delete_channel(channel_id)
    return jsonify({'status': 'success', 'name': channel_id})

@app.route('/create_message', methods=['POST'])
def create_message():
    message = request.get_json().get('message')
    print(f"recieved message {message}")
    database.create_message(get_current_channel(), message)
    return jsonify({'status': 'success', 'message': message})

def get_current_channel():
    global current_channel
    return current_channel

def set_current_channel(channel_id):
    global current_channel
    print(f"Updating current_channel; prev: {current_channel}, next: {channel_id}")
    current_channel = channel_id

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

