import os
import sys
from sqlalchemy import ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship, declarative_base, Mapped, mapped_column
from sqlalchemy import create_engine
from eralchemy2 import render_er
from datetime import datetime

Base = declarative_base()

class Usuario(Base):
    __tablename__ = 'usuario'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nombre: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    contraseña: Mapped[str] = mapped_column(String(200), nullable=False)
    fecha_creacion: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)

    posts = relationship('Post', backref='usuario', lazy=True)
    comentarios = relationship('Comentario', backref='usuario', lazy=True)
    likes = relationship('Likes', backref='usuario', lazy=True)

class Post(Base):
    __tablename__ = 'post'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    usuario_id: Mapped[int] = mapped_column(Integer, ForeignKey('usuario.id'), nullable=False)
    imagen: Mapped[str] = mapped_column(String(200), nullable=False)
    descripcion: Mapped[str] = mapped_column(String(500))
    fecha_publicacion: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)

    comentarios = relationship('Comentario', backref='post', lazy=True)
    likes = relationship('Like', backref='post', lazy=True)

class Comentario(Base):
    __tablename__ = 'comentario'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    usuario_id: Mapped[int] = mapped_column(Integer, ForeignKey('usuario.id'), nullable=False)
    post_id: Mapped[int] = mapped_column(Integer, ForeignKey('post.id'), nullable=False)
    contenido: Mapped[str] = mapped_column(String(500), nullable=False)
    fecha_comentario: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)

class Like(Base):
    __tablename__ = 'like'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    usuario_id: Mapped[int] = mapped_column(Integer, ForeignKey('usuario.id'), nullable=False)
    post_id: Mapped[int] = mapped_column(Integer, ForeignKey('post.id'), nullable=False)
    
    
engine = create_engine('sqlite:///instagram_clone.db')
Base.metadata.create_all(engine)

## Draw from SQLAlchemy base
try:
    result = render_er(Base, 'diagram.png')
    print("Success! Check the diagram.png file")
except Exception as e:
    print("There was a problem genering the diagram")
    raise e
