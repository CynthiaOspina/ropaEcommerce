from flask import redirect, render_template, url_for, flash, request, session, current_app
from app import db, app, photos, search, bcrypt, login_manager
from .forms import RegistroCliente, LoginClientForm
from .models import Registro, OrdenCliente
from flask_login import login_required, current_user, logout_user, login_user
import secrets, os

@app.route('/cliente/registro', methods=['GET','POST'])
def registro_cliente():
    form = RegistroCliente()
    if form.validate_on_submit():
        hash_password = bcrypt.generate_password_hash(form.password.data)
        register = Registro(name=form.name.data,username=form.username.data,email=form.email.data,password=hash_password,country=form.country.data,state=form.state.data,
                            city=form.city.data,address=form.address.data,zipcode=form.zipcode.data)
        db.session.add(register)
        flash(f'Bienvenido {form.name.data} gracias por registrarse! ','success')
        db.session.commit()
        return redirect(url_for('customerLogin'))
    return render_template('cliente/registro.html', form=form)

@app.route('/cliente/login', methods=['POST','GET'])
def customerLogin():
    form = LoginClientForm()
    if form.validate_on_submit():
        user = Registro.query.filter_by(email = form.email.data).first()
        if user and bcrypt.check_password_hash(user.password , form.password.data):
            login_user(user)
            flash('Te encuentras logueado!', 'success')
            next = request.args.get('next')
            return redirect(next or url_for('home'))
        flash('Email o Clave errada','danger')
        return redirect(url_for('customerLogin'))

    return render_template('cliente/login.html', form=form)

@app.route('/cliente/logout')
def cliente_logout():
    logout_user()
    return redirect(url_for('customerLogin'))

@app.route('/getorder')
@login_required
def get_order():
    if current_user.is_authenticated:
        cliente_id = current_user.id
        factura = secrets.token_hex(5)
        session['monto']=0
        try:
            order = OrdenCliente(factura=factura, cliente_id=cliente_id, orden=session['Shoppingcart'],monto=session['monto'])
            db.session.add(order)
            db.session.commit()
            session.pop('Shoppingcart')
            session.pop('monto')
            flash('Tu orden ha sido creada', 'success')
            return redirect(url_for('ordenes', factura=factura))
        except Exception as e:
            print(e)
            flash('Error durante la generación de su orden', 'danger')
            return redirect(url_for('getCart'))

@app.route('/orden/<factura>')
@login_required
def ordenes(factura):
    if current_user.is_authenticated:
        grandTotal = 0
        subTotal = 0
        cliente_id = current_user.id
        cliente = Registro.query.filter_by(id=cliente_id).first()
        ordenes = OrdenCliente.query.filter_by(cliente_id = cliente_id).order_by(OrdenCliente.id.desc()).first()
        for _key, product in ordenes.orden.items():
            descuento = (product['discount']/100 * float(product['price']))
            subTotal += float(product['price']) * int(product['quantity'])
            subTotal -= descuento
            tax = ("%.2f" % (.18 * float(subTotal)))
            grandTotal = float("%.2f" % (1.18 * subTotal))

    else:
        return redirect(url_for('customerLogin'))
    return render_template('cliente/orden.html', factura = factura, tax=tax, subTotal=subTotal, grandTotal=grandTotal, cliente=cliente, ordenes=ordenes)

@app.route('/orden1/<factura>')
@login_required
def ordenes1(factura):
    if current_user.is_authenticated:
        grandTotal = 0
        subTotal = 0
        cliente_id = current_user.id
        cliente = Registro.query.filter_by(id=cliente_id).first()
        ordenes = OrdenCliente.query.filter_by(factura = factura).first()
        for _key, product in ordenes.orden.items():
            descuento = (product['discount']/100 * float(product['price']))
            subTotal += float(product['price']) * int(product['quantity'])
            subTotal -= descuento
            tax = ("%.2f" % (.18 * float(subTotal)))
            grandTotal = float("%.2f" % (1.18 * subTotal))

    else:
        return redirect(url_for('customerLogin'))
    return render_template('cliente/orden.html', factura = factura, tax=tax, subTotal=subTotal, grandTotal=grandTotal, cliente=cliente, ordenes=ordenes)

@app.route('/pago/<factura>')
@login_required
def pago(factura):
    if current_user.is_authenticated:
        grandTotal = 0
        subTotal = 0
        cliente_id = current_user.id
        cliente = Registro.query.filter_by(id=cliente_id).first()
        ordenes = OrdenCliente.query.filter_by(factura = factura).first()
        for _key, product in ordenes.orden.items():
            descuento = (product['discount']/100 * float(product['price']))
            subTotal += float(product['price']) * int(product['quantity'])
            subTotal -= descuento
            tax = ("%.2f" % (.18 * float(subTotal)))
            grandTotal = ("%.2f" % (1.18 * subTotal))

    else:
        return redirect(url_for('customerLogin'))
    return render_template('cliente/pago.html', factura = factura, tax=tax, subTotal=subTotal, grandTotal=grandTotal, cliente=cliente, ordenes=ordenes)

@app.route('/pagar/<factura>', methods=['POST'])
@login_required
def pagar(factura):
    if current_user.is_authenticated:
            grandTotal = 0
            subTotal = 0
            cliente_id = current_user.id
            cliente = Registro.query.filter_by(id=cliente_id).first()
            ordenes = OrdenCliente.query.filter_by(factura = factura).first()
            ordenes.status = "completado"
            for _key, product in ordenes.orden.items():
                descuento = (product['discount']/100 * float(product['price']))
                subTotal += float(product['price']) * int(product['quantity'])
                subTotal -= descuento
                tax = ("%.2f" % (.18 * float(subTotal)))
                grandTotal = ("%.2f" % (1.18 * subTotal))
            db.session.commit()    

    else:
        return redirect(url_for('customerLogin'))
    return render_template('cliente/pagado.html', factura = factura, tax=tax, subTotal=subTotal, grandTotal=grandTotal, cliente=cliente, ordenes=ordenes)






