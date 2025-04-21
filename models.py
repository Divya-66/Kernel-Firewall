from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class BlockedIP(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ip = db.Column(db.String(15), nullable=False)
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())

class Log(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())