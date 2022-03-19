from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'test.db'
db = SQLAlchemy(app)

class Producto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(80), nullable=False)
    precio = db.Column(db.Float(15),  nullable=False)

class Pedido(db.Model):
    id=db.Colum(db.Integer, primary_key=True)
    fecha=db.Colum(db.DateTime, nullable=False,
        default=datetime.utcnow)

class Productos(db.Model):
    id=db.Colum(db.Integer, primary_key=True)
    fk_producto=db.Column(db.Integer, db.ForeignKey('producto.id'),
        nullable=False)
    fk_pedido=db.Column(db.Integer, db.ForeignKey('pedido.id'),
        nullable=False)


