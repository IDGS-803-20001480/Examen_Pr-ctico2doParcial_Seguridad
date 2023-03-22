#Importamos la clase Blueprint del módulo flask
from flask import Blueprint, render_template
#Importamos login_required, current_user de flask_security
from flask_security import login_required, current_user
#Importamos el decorador login_required de flask_security
from flask_security.decorators import roles_required,roles_accepted
#Importamos el objeto de la BD desde __init__.py
from . import db
#Importamos el modelo producto
from .models import Product


main = Blueprint('main',__name__)

#Definimos la ruta a la página principal
@main.route('/')
def index():
    return render_template('index.html')

#Definimos la ruta a la página de perfil
@main.route('/profile')
@login_required
#restringuimos que solo los de rol admin puedan acceder a esta ruta o a todos los que se encuentren en la lista de todos roles 
#@roles_required('admin')
#el acceppted acepta todos los roles que se encuentren en la lista de roles
#@roles_accepted('admin','user')
def profile():
    return render_template('profile.html', name=current_user.name)

#Definimos la ruta a la página de productos
@main.route('/products')
#@login_required
@roles_required('user')
def products():
    productos = Product.query.all()
    return render_template('products.html', productos=productos)

@main.route('/contacto')
def contacto():
    return render_template('contacto.html')