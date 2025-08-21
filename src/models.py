from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List

db = SQLAlchemy()

# Tabla de Usuarios
class User(db.Model):
    __tablename__ = 'user'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False) 
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False, default=True) 
    user_name: Mapped[str] = mapped_column(String(50), nullable=False, unique=True) 
    profile_pic: Mapped[str] = mapped_column(String(255), nullable=True)
    bio: Mapped[str] = mapped_column(String(255), nullable=True) # 

    posts: Mapped[List["Post"]] = relationship(back_populates="author", cascade="all, delete-orphan")
    comments: Mapped[List["Comment"]] = relationship(back_populates="user")
    likes: Mapped[List["Like"]] = relationship(back_populates="user")
    followers: Mapped[List["Follow"]] = relationship(foreign_keys='Follow.followed_id', back_populates="followed")
    following: Mapped[List["Follow"]] = relationship(foreign_keys='Follow.follower_id', back_populates="follower")
    
    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "user_name": self.user_name,
            "profile_pic": self.profile_pic,
            "bio": self.bio,
        }

# Tabla de Publicaciones
class Post(db.Model):
    __tablename__ = 'post'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    media: Mapped[str] = mapped_column(String(255), nullable=False)
    caption: Mapped[str] = mapped_column(String(500), nullable=True)

    author: Mapped["User"] = relationship(back_populates="posts")
    comments: Mapped[List["Comment"]] = relationship(back_populates="post", cascade="all, delete-orphan")
    likes: Mapped[List["Like"]] = relationship(back_populates="post", cascade="all, delete-orphan")
    
    def serialize(self):
        return {
            "id": self.id,
            "media": self.media,
            "caption": self.caption,
            "author_id": self.user_id 
        }

# Tabla de Comentarios
class Comment(db.Model):
    __tablename__ = 'comment'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True) 
    post_id: Mapped[int] = mapped_column(ForeignKey("post.id"), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    text: Mapped[str] = mapped_column(String(300), nullable=False)

    user: Mapped["User"] = relationship(back_populates="comments")
    post: Mapped["Post"] = relationship(back_populates="comments")
    
    def serialize(self):
        return {
            "id": self.id,
            "post_id": self.post_id,
            "user_id": self.user_id,
            "text": self.text,
        }

# Tabla de Me Gusta (Likes)
class Like(db.Model): 
    __tablename__ = 'like'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True) 
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    post_id: Mapped[int] = mapped_column(ForeignKey("post.id"), nullable=False)

    user: Mapped["User"] = relationship(back_populates="likes")
    post: Mapped["Post"] = relationship(back_populates="likes")

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "post_id": self.post_id
        }

# Tabla de Seguimientos (Follow)
class Follow(db.Model): 
    __tablename__ = 'follow'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    follower_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    followed_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)

    follower: Mapped["User"] = relationship(foreign_keys=[follower_id], back_populates="following")
    followed: Mapped["User"] = relationship(foreign_keys=[followed_id], back_populates="followers")

    def serialize(self):
        return {
            "id": self.id,
            "follower_id": self.follower_id,
            "followed_id": self.followed_id,
        }