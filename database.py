from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship

# Define the base for declarative class definitions
Base = declarative_base()

class Channel(Base):
    __tablename__ = 'channels'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    messages = relationship("Message", back_populates="channel", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Channel(id={self.id}, name='{self.name}')>"

class Message(Base):
    __tablename__ = 'messages'
    id = Column(Integer, primary_key=True)
    content = Column(String, nullable=False)
    channel_id = Column(Integer, ForeignKey('channels.id'), nullable=False)
    channel = relationship("Channel", back_populates="messages")

    def __repr__(self):
        return f"<Message(id={self.id}, content='{self.content}', channel_id={self.channel_id})>"


class Database:
    """Manages database operations for channels and messages."""
    def __init__(self, db_url='sqlite:///channels_messages.db'):
        """Initializes the database, engine, and session."""
        self.engine = create_engine(db_url)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()
        
        # Intent tracking for deleting channels
        self.channel_intent_count = 0
        self.prev_channel_intent_id = -1

    def __handle_delete_channel_request__(self, channel_id):
        """Private helper to delete a channel from the database."""
        channel_to_delete = self.session.query(Channel).filter(Channel.id == channel_id).first()
        if channel_to_delete:
            self.session.delete(channel_to_delete)
            self.session.commit()
            print(f"Channel with ID '{channel_id}' and its messages deleted.")
        else:
            print(f"Channel with ID '{channel_id}' not found.")

    def __handle_delete_message_request__(self, message_id):
        """Private helper to delete a message from the database."""
        message_to_delete = self.session.query(Message).filter(Message.id == message_id).first()
        if message_to_delete:
            self.session.delete(message_to_delete)
            self.session.commit()
            print(f"Message with ID '{message_id}' deleted.")
        else:
            print(f"Message with ID '{message_id}' not found.")

    def create_channel(self, name):
        """Creates and saves a new channel."""
        new_channel = Channel(name=name)
        self.session.add(new_channel)
        self.session.commit()
        print(f"Channel '{name}' created with ID {new_channel.id}.")
        return new_channel

    def delete_channel(self, channel_id):
        """Confirms intent and deletes a channel if called multiple times."""
        print(f"Attempting to delete channel {channel_id}...")
        if self.channel_intent_count >= 1 and channel_id == self.prev_channel_intent_id:
            print(f"Confirmed intent. Deleting channel {channel_id}.")
            self.__handle_delete_channel_request__(channel_id)
            self.channel_intent_count = 0 
            self.prev_channel_intent_id = -1
        elif channel_id == self.prev_channel_intent_id:
            self.channel_intent_count += 1
            print(f"Call delete_channel for ID {channel_id} again to confirm.")
        else:
            self.channel_intent_count = 1
            self.prev_channel_intent_id = channel_id
            print(f"This is the first request for channel ID {channel_id}. Call again to confirm deletion.")

    def get_channels(self):
        """Returns a list of all channels."""
        return self.session.query(Channel).all()

    def create_message(self, channel_id, content):
        """Creates a new message within a specified channel."""
        # First, check if the channel exists
        channel = self.session.query(Channel).filter(Channel.id == channel_id).first()
        if not channel:
            print(f"Error: Channel with ID {channel_id} not found. Cannot create message.")
            return None
        
        new_message = Message(content=content, channel_id=channel_id)
        self.session.add(new_message)
        self.session.commit()
        print(f"Message '{content}' added to channel {channel_id}.")
        return new_message

    def delete_message(self, message_id):
        """Deletes a message directly from the database."""
        self.__handle_delete_message_request__(message_id)

    def get_messages(self, channel_id):
        """Returns all messages for a given channel ID."""
        return self.session.query(Message).filter(Message.channel_id == channel_id).all()

    def close_session(self):
        """Closes the database session."""
        self.session.close()