from typing import Optional
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from app import db
from app import login

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class User(UserMixin, db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(64), index=True, unique=True)
    email: Mapped[str] = mapped_column(String(120), index=True, unique=True)
    passowrd_hash: Mapped[Optional[str]] = mapped_column(String(256))

    def set_password(self, password):
        self.passowrd_hash = generate_password_hash(password, method='pbkdf2')

    def check_password(self, password):
        return check_password_hash(self.passowrd_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'
    
@login.user_loader
def load_user(id):
    return db.session.get(User, int(id))