from flask import Flask, render_template, request, jsonify

from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from database import Database

app = Flask(__name__)
database = Database()

@app.route('/')
def home():
    #database.create_new_channel("test channel")
    channels = database.get_channels()
    channel_names = [channel.name for channel in channels]

    return render_template('index.html', channels=channels)

@app.route('/channel_clicked', methods=['POST'])
def channel_clicked():
    channel_id = request.get_json().get('id')

    print(f"Channel {channel_id} clicked.")

    return jsonify({'status': 'success', 'id': channel_id})

if __name__ == '__main__':
    app.run(debug=True)