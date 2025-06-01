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

    def create_new_channel(self, name):
        new_channel = Channel(name=name)
        self.session.add(new_channel)
        self.session.commit()
        print(f"Channel '{name}' created.")

    def get_channels(self):
        return self.session.query(Channel).all()

    def close_session(self):
        self.session.close()  # Close the session when done