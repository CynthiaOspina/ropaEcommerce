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
        customer_id = current_user.id
        factura = secrets.token_hex(5)
        try:
            order = OrdenCliente(factura=factura, customer_id=customer_id, orden=session['Shoppingcart'])
            db.session.add(order)
            flash('Tu orden ha sido creada', 'success')
            return redirect(url_for('home'))
        except Exception as e:
            print(e)
            flash('Error durante la generación de su orden', 'danger')
            redirect(url_for('getCart'))