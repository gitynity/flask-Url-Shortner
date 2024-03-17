from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class URL(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    long_url = db.Column(db.String(500), nullable=False)
    short_url = db.Column(db.String(10), nullable=False, unique=True)
