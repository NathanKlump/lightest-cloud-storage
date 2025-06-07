from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Define the base for declarative class definitions
Base = declarative_base()

class Channel(Base):
    __tablename__ = 'channels'
    id = Column(Integer, primary_key=True)
    name = Column(String)

class Database:
    def __init__(self, db_url='sqlite:///channels_messages.db'):
        self.engine = create_engine(db_url)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()  # Create a session for reuse
        self.intent_count = 0
        self.prev_intent_id = -1

    def __handle_delete_request__(self, channel_id):
        channel_to_delete = self.session.query(Channel).filter(Channel.id == channel_id).first()
        if channel_to_delete:
            self.session.delete(channel_to_delete)
            self.session.commit()
            print(f"Channel with ID '{channel_id}' deleted.")
        else:
            print(f"Channel with ID '{channel_id}' not found.")

    def create_new_channel(self, name):
        new_channel = Channel(name=name)
        self.session.add(new_channel)
        self.session.commit()
        print(f"Channel '{name}' created.")

    def delete_channel(self, channel_id):
        '''this determines if the action was intended and deletes the channel'''
        print(f"{channel_id} {self.prev_intent_id}")
        if self.intent_count > 1 and channel_id == self.prev_intent_id:
            print(f"deleting channel {channel_id}")
            self.__handle_delete_request__(channel_id)
            self.intent_count = 0 #reset after deletion
            self.prev_intent_id = -1 #reset after deletion
            return
        elif channel_id == self.prev_intent_id: 
            print(f"incrementing intent {self.intent_count}")
            self.intent_count += 1
        else:
            self.intent_count = 1 #reset after getting a different intent id
            self.prev_intent_id = channel_id #set a new intent id

    def get_channels(self):
        return self.session.query(Channel).all()

    def close_session(self):
        self.session.close()  # Close the session when done