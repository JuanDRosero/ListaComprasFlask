import os.path
from flask import Flask, request, render_template, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import sys

app = Flask(__name__)

dir_folder = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(dir_folder, "test.db"))

app.config['SQLALCHEMY_DATABASE_URI'] = database_file
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# Funciones CRUD
def create_product(name, price):
    product = Producto(nombre=name, precio=price)
    db.session.add(product)
    db.session.commit()
    db.session.refresh(product)

#agregar fecha default
def create_order(products, date):
    order = Pedido(fecha=datetime.strptime(date, '%Y-%m-%d'), total=sum([p.precio for p in products]))
    for product in products:
        order.productos.append(product)

    db.session.add(order)
    db.session.commit()
    db.session.refresh(order)

def get_product_by_id(product_id):
    return db.session.query(Producto).filter_by(id=product_id).first()

def read_products():
    return db.session.query(Producto).all()

def read_orders():
    orders = db.session.query(Pedido).all()
    return db.session.query(Pedido).all()

def update_product(product_id, name, price):
    db.session.query(Producto).filter_by(id=product_id).update({
        "nombre": name,
        "precio": price
    })
    db.session.commit()


def delete_product(product_id):
    db.session.query(Producto).filter_by(id=product_id).delete()
    db.session.commit()

def delete_product_list(order_id):
    db.session.query(Pedido).filter_by(id=order_id).delete()
    db.session.query(ProductoPedido).filter_by(fk_pedido=order_id).delete()
    db.session.commit()


# Rutas
@app.route("/lista", methods=["POST", "GET"])
def add_list():
    selected_products = []
    if request.method == "POST":
        for value in request.form.getlist('check'):
            print("value: ", end=value)
            selected_products.append(get_product_by_id(value))
        create_order(selected_products, request.form['fecha'])
    return render_template("lista.html", products=read_products())

@app.route("/producto", methods=["POST", "GET"])
def add_product():
    if request.method == "POST":
        create_product(request.form['nombre'], request.form['precio'])
    return render_template("producto.html")

@app.route("/productos")
def view_all_products():
    return render_template("productos.html", products=read_products())

@app.route("/", methods=["POST", "GET"])
def view_index():
    return render_template("index.html", orders=read_orders())

@app.route("/<order_id>", methods=["POST", "GET"])
def edit_list(order_id):
    if request.method == "GET":
        delete_product_list(order_id)
    return render_template("index.html", orders=read_orders())

@app.route("/editar/<product_id>", methods=["POST", "GET"])
def edit_product(product_id):
    if request.method == "POST":
        update_product(product_id, name=request.form['nombre'], price=request.form['precio'])
        print(request.form['nombre'], file=sys.stderr)
    elif request.method == "GET":
        delete_product(product_id)
    return redirect("/productos", code=302)

class Producto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(80), nullable=False)
    precio = db.Column(db.Float(15),  nullable=False)
    pedidos = db.relationship('Pedido', secondary='producto_pedido')

class Pedido(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    fecha=db.Column(db.DateTime, nullable=False,
        default=datetime.utcnow)
    productos = db.relationship('Producto', secondary='producto_pedido')
    total=db.Column(db.Float(15),  nullable=False)

class ProductoPedido(db.Model):
    __tablename__ = 'producto_pedido'
    fk_producto=db.Column(db.Integer, db.ForeignKey('producto.id'),
        nullable=False, primary_key=True)
    fk_pedido=db.Column(db.Integer, db.ForeignKey('pedido.id'),
        nullable=False, primary_key=True)

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)