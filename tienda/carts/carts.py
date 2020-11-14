from flask import redirect, render_template, url_for, flash, request, session, current_app
from app import db, app
from tienda.products.models import Product
import json, decimal
from tienda.admin.rutas import brandsF, categories
from tienda.cliente.models import OrdenCliente
from flask_login import login_required, current_user, logout_user, login_user

class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            # wanted a simple yield str(o) in the next line,
            # but that would mean a yield on the line with super(...),
            # which wouldn't work (see my comment below), so...
            return (str(o) for o in [o])
        return super(DecimalEncoder, self).default(o)

def MagerDicts(dict1, dict2):
    if isinstance(dict1, list) and isinstance(dict2, list):
        return dict1 + dict2
    elif isinstance(dict1,dict) and isinstance(dict2,dict):
        return dict(list(dict1.items()) + list(dict2.items()))
    return False

@app.route('/addcart', methods=['POST','GET'])
def addcart():
    try:
        product_id = request.form.get('product_id')
        quantity = request.form.get('quantity')
        colors = request.form.get('colors')
        product = Product.query.filter_by(id=product_id).first()
        if product_id and quantity and colors and request.method == 'POST':
            session['monto'] = product.price * product.quantity
            DictItems = {
                product_id : {
                    'name' : product.name,
                    'price' : str(product.price),
                    'discount' : product.discount,
                    'color' : colors,
                    'quantity' : quantity,
                    'image' : product.image_1,
                    'colors' : product.colors
                }
            }
            if 'Shoppingcart' in session:
                print(session['Shoppingcart'])
                if product_id in session['Shoppingcart']:
                    if product_id in session['Shoppingcart']:
                        for key, item in session['Shoppingcart'].items():
                            if int(key) == int(product_id):
                                session.modified = True
                                item['quantity'] = str(int(item['quantity']) + 1)
                                flash('Se añadió la cantidad de +1 del item seleccionado','success')
                else:
                    session['Shoppingcart'] = MagerDicts(session['Shoppingcart'], DictItems)
                    return redirect(request.referrer)
            else:
                session['Shoppingcart'] = DictItems
                return redirect(request.referrer)


    except Exception as e:
        print(e)
    finally:
        return redirect(request.referrer)


@app.route('/carts')
def getCart():
    if 'Shoppingcart' not in session or len(session['Shoppingcart']) <= 0:
        return redirect(url_for('home'))
    subtotal = 0
    grandtotal = 0

    for key, product in session['Shoppingcart'].items():
        precio = 0
        try:
            if product['price']:
                precio = float(product['price'])
            else:
                precio = 0
        except Exception as e:
            precio = 0

        discount = (product['discount']/100 * float(precio))
        subtotal += float(precio) * int(product['quantity'])
        subtotal -= discount
        tax = ("%.2f" % (.18 * float(subtotal)))
        grandtotal = float("%.2f" % (1.06 * subtotal))
    return render_template('products/carts.html', tax = tax, grandtotal = grandtotal, brands=brandsF(), categories=categories())

@app.route('/ordenes')
def getOrdenes():
    ordenes = db.session.query(OrdenCliente).filter_by(cliente_id=current_user.id).all()
    return render_template('products/ordenes.html', ordenes = ordenes)

@app.route('/vaciarCarrito')
def empty_cart():
    try:
        session.pop('Shoppingcart', None)
        return redirect(url_for('home'))
    except Exception as e:
        print(e)

@app.route('/updatecart/<int:code>', methods=['POST'])
def updatecart(code):
    if 'Shoppingcart' not in session and len(session['Shoppingcart']) <= 0:
        return redirect(url_for('home'))
    if request.method == 'POST':
        quantity = request.form.get('quantity')
        color = request.form.get('color')
        try:
            session.modified = True
            for key, item in session['Shoppingcart'].items():
                if int(key) == code:
                    item['quantity'] = quantity
                    item['color'] = color
                    flash('Item actualizado!','success')
                    return redirect(url_for('getCart'))
        except Exception as e:
            print(e)
            return redirect(url_for('getCart'))

    return

@app.route('/deleteitem/<int:id>')
def deleteitem(id):
    if 'Shoppingcart' not in session and len(session['Shoppingcart']) <= 0:
        return redirect(url_for('home'))
    try:
        session.modified = True
        for key, item in session['Shoppingcart'].items():
            if int(key) == id:
                session['Shoppingcart'].pop(key, None)
                return redirect(url_for('getCart'))
    except Exception as e:
        print(e)
        return redirect(url_for('getCart'))
