import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy import create_engine
from eralchemy2 import render_er
from sqlalchemy import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from datetime import datetime

Base = declarative_base()

class Usuario(Base):
    __tablename__ = 'usuario'
    id = mapped_column(Integer, primary_key=True)
    nombre = mapped_column(String(100), nullable=False)
    email = mapped_column(String(100), unique=True, nullable=False)
    contrasena = mapped_column(String(200), nullable=False)
    fecha_creacion = mapped_column(DateTime, default=datetime.now)
    biografia = mapped_column(String(500))
    foto_perfil = mapped_column(String(200))

    posts = relationship('Post', backref='usuario', lazy=True)
    comentarios = relationship('Comentario', backref='usuario', lazy=True)
    seguidores = relationship('Seguidor', backref='seguidor', lazy=True)

    def __repr__(self):
        return f'<Usuario {self.nombre}>'
    
class Post(Base):
    __tablename__ = 'post'
    id = Column(Integer, primary_key=True)
    usuario_id = Column(Integer, ForeignKey('usuario.id'), nullable=False)
    titulo = Column(String(100), nullable=False)
    contenido = Column(String(500))
    fecha_publicacion = Column(DateTime, default=datetime.now)
    imagen = Column(String(200))
    likes = Column(Integer, default=0)

    comentarios = relationship('Comentario', backref='post', lazy=True)

    def __repr__(self):
        return f'<Post {self.titulo}>'

class Comentario(Base):
    __tablename__ = 'comentario'
    post_id = Column(Integer, ForeignKey('post.id'), nullable=False)
    usuario_id = Column(Integer, ForeignKey('usuario.id'), nullable=False)
    contenido = Column(String(500), nullable=False)
    fecha_comentario = Column(DateTime, default=datetime.now)

    def __repr__(self):
        return f'<Comentario {self.id}>'
    
class Seguidor(Base):
    __tablename__ = 'seguidor'
    id = Column(Integer, primary_key=True)
    seguidor_id = Column(Integer, ForeignKey('usuario.id'), nullable=False)
    seguido_id = Column(Integer, ForeignKey('usuario.id'), nullable=False)

    def __repr__(self):
        return f'<Seguidor {self.seguidor_id} sigue a {self.seguido_id}>'
    
    
engine = create_engine('sqlite:///instagram_clone.db')
Base.metadata.create_all(engine)

## Draw from SQLAlchemy base
try:
    result = render_er(Base, 'diagram.png')
    print("Success! Check the diagram.png file")
except Exception as e:
    print("There was a problem genering the diagram")
    raise e
