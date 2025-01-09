from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import logging

class Database:
    def __init__(self, db_url='sqlite:///data/db.db'):
        """
        Initierar databasanslutning och session.
        :param db_url: Sträng för databasanslutning (default: SQLite i projektroten).
        """
        self.db_url = db_url
        self.engine = create_engine(self.db_url)
        self.Session = sessionmaker(bind=self.engine)
        self.session = None

    def initialize(self, base):
        """Skapar alla tabeller i databasen."""
        base.metadata.create_all(self.engine)
        logging.info("Databastabeller skapade.")

    def connect(self):
        """Startar en ny session."""
        if self.session is None:
            self.session = self.Session()
        logging.info("Databasen ansluten.")

    def disconnect(self):
        """Stänger den aktiva sessionen."""
        if self.session:
            self.session.close()
            self.session = None
        logging.info("Databasen frånkopplad.")

    def add(self, instance):
        """Lägger till en enskild instans i databasen."""
        self.session.add(instance)
        self.session.commit()

    def add_all(self, instances):
        """Lägger till flera instanser i databasen."""
        self.session.add_all(instances)
        self.session.commit()

    def query(self, model):
        """Returnerar en query-objekt för den angivna modellen."""
        return self.session.query(model)
