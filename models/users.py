import uuid

# absolute or relative import
# relative (current) import | . current folder & .. one folder up
# from ..extensions import db

# absolute (project) import
from extensions import db
from flask_login import UserMixin


class User(UserMixin, db.Model):  # added usermixin for isactive
    __tablename__ = "users"
    id = db.Column(db.String(50), primary_key=True, default=lambda: str(uuid.uuid4()))
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(200))

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "password": self.password,
        }
