from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from service import app

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///accounts.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class DataValidationError(Exception):
    pass

class Account(db.Model):
    __tablename__ = 'accounts'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    email = db.Column(db.String(128))
    address = db.Column(db.String(256))
    phone_number = db.Column(db.String(32))
    date_joined = db.Column(db.Date)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "address": self.address,
            "phone_number": self.phone_number,
            "date_joined": str(self.date_joined) if self.date_joined else None
        }

    def deserialize(self, data):
        if not isinstance(data, dict):
            raise DataValidationError("Invalid data")
        self.name = data.get("name", self.name)
        self.email = data.get("email", self.email)
        self.address = data.get("address", self.address)
        self.phone_number = data.get("phone_number", self.phone_number)
        return self

    def create(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find(cls, account_id):
        return cls.query.get(account_id)

    @classmethod
    def all(cls):
        return cls.query.all()
