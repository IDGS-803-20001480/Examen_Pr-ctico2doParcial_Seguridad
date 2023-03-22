from flask import Blueprint,render_template,redirect, request,url_for
#Importamos el decorador login_required de flask_security
from flask_security.decorators import roles_required,roles_accepted
from .models import Product
from . import db
import base64

productos = Blueprint('productos',__name__)

@productos.route('/getproducts', methods=['GET'])
@roles_required('admin')
def getproducts():
    productos = Product.query.all()
    return render_template('administracion/productList.html', productos=productos)

@productos.route('/addproduct', methods=['GET','POST'])
@roles_required('admin')
def addproduct():
    if request.method == 'POST':
        print(request.files['image'])
        imagenR= request.files['image']
        imagen = base64.b64encode(imagenR.read())
        product = Product(
            name=request.form['name'],
            description=request.form['description'], 
            price=request.form['price'],
            image=imagen,
            stock=request.form['stock'])
        db.session.add(product)
        db.session.commit()
        return redirect(url_for('productos.getproducts'))
    return render_template('administracion/productCreate.html')

@productos.route('/updateproduct', methods=['GET','POST'])
@roles_required('admin')
def updateproduct():
    if request.method == 'GET':
        id = request.args.get('id')
        product = db.session.query(Product).filter(Product.id == id).first()
        id = product.id
        name = product.name
        description = product.description
        price = product.price
        image = product.image
        stock = product.stock
        return render_template('administracion/productUpdate.html', id=id, name=name, description=description, price=price, image=image, stock=stock)
    
    if request.method == 'POST':
        if request.files['image'] != "":    
            imagenR= request.files['image']
            imagen = base64.b64encode(imagenR.read())
            id = request.form['id']
            product = db.session.query(Product).filter(Product.id == id).first()
            product.name = request.form['name']
            product.description = request.form['description']
            product.price = request.form['price']
            product.image = imagen
            product.stock = request.form['stock']
            db.session.add(product)
            db.session.commit()
            return redirect(url_for('productos.getproducts'))
        else:
            id = request.form['id']
            product = db.session.query(Product).filter(Product.id == id).first()
            product.name = request.form['name']
            product.description = request.form['description']
            product.price = request.form['price']
            product.stock = request.form['stock']
            db.session.add(product)
            db.session.commit()
            return redirect(url_for('productos.getproducts'))

@productos.route('/deleteproduct', methods=['GET','POST'])
@roles_required('admin')
def deleteproduct():
    if request.method == 'GET':
        id = request.args.get('id')
        product = db.session.query(Product).filter(Product.id == id).first()
        db.session.delete(product)
        db.session.commit()
        return redirect(url_for('productos.getproducts'))
    else:
        return redirect(url_for('productos.getproducts'))