from app import db

track = db.Table(
    "track",
    db.Column(
        "user_id", db.Integer, db.ForeignKey("user.id"), primary_key=True
    ),
    db.Column(
        "item_id", db.Integer, db.ForeignKey("item.id"), primary_key=True
    ),
)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    messenger_id = db.Column(db.BigInteger, nullable=False)
    items = db.relationship(
        "Item", cascade="all,delete", secondary="track", backref="users"
    )


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    price = db.Column(db.Float, nullable=False)
    url = db.Column(db.String(500), nullable=False)
