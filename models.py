from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

track = db.Table(
    "track",
    db.Column("user_id", db.Integer, db.ForeignKey("user.id")),
    db.Column("item_id", db.Integer, db.ForeignKey("item.id")),
)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    messenger_id = db.Column(db.String(200), nullable=False)
    items = db.relationship("Item", secondary="track", backref="users", lazy="True")


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Float, nullable=False)
    url = db.Column(db.String(500), nullable=False)
