from flask import render_template, session, request, redirect, url_for, flash
from app import app, db, bcrypt
from .forms import RegistrationForm, LoginForm
from tienda.products.models import Brand, Category, Product
from .models import User

def brandsF():
    brands = Brand.query.join(Product, (Brand.id == Product.brand_id)).all()
    return brands

def categories():
    categories = Category.query.join(Product, (Category.id == Product.category_id)).all()
    return categories

@app.route('/')
def home():
    page = request.args.get('page', 1, type=int)
    products = Product.query.filter(Product.stock > 0).order_by(Product.id.desc()).paginate(page=page, per_page=8)
    return render_template('products/index.html', products=products, brands=brandsF(), categories=categories())

@app.route('/product/<int:id>')
def single_page(id):
    product = Product.query.get_or_404(id)
    return render_template('products/single_page.html', product=product, brands=brandsF(), categories=categories())

@app.route('/marca/<int:id>')
def get_brand(id):
    page = request.args.get('page', 1, type=int)
    get_brand = Category.query.filter_by(id=id).first_or_404()
    brand = Product.query.filter_by(brand=get_brand).paginate(page=page, per_page=8)
    return render_template('products/index.html', brand=brand, brands=brandsF(), categories=categories(), get_brand=get_brand)

@app.route('/categories/<int:id>')
def get_category(id):
    page = request.args.get('page', 1, type=int)
    get_cat = Category.query.filter_by(id=id).first_or_404()
    get_cat_prod = Product.query.filter_by(category=get_cat).paginate(page=page, per_page=8)
    return render_template('products/index.html', get_cat_prod=get_cat_prod, brands=brandsF(), categories=categories(), get_cat=get_cat)

@app.route('/admin')
def admin():
    if 'email' not in session:
        flash(f'Porfavor ingrese primero','danger')
        return redirect(url_for('login'))
    products = Product.query.all()
    return render_template('admin/index.html', title='Admin Page', products=products)

@app.route('/marca')
def brands():
    if 'email' not in session:
        flash(f'Porfavor ingrese primero','danger')
        return redirect(url_for('login'))
    brands = Brand.query.order_by(Brand.id.desc()).all()
    return render_template('admin/marca.html', title='Pagina de Marcas', brands=brands)

@app.route('/categoria')
def category():
    if 'email' not in session:
        flash(f'Porfavor ingrese primero','danger')
        return redirect(url_for('login'))
    categories = Category.query.order_by(Category.id.desc()).all()
    return render_template('admin/marca.html', title='Pagina de Marcas', categories=categories)

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        hash_password = bcrypt.generate_password_hash(form.password.data)
        user = User( name=form.username.data,
                     username=form.email.data,
                     email=form.email.data,
                     password=hash_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Bienvenido {form.name.data} gracias por registrarse','success')
        return redirect(url_for('login'))
    return render_template("admin/registro.html", form=form, title="Registrar Usuario")

@app.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User.query.filter_by(email = form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            session['email'] = form.email.data
            flash(f'Bienvenido {form.email.data}, acabas de ingresar!', 'success')
            return redirect(request.args.get('next') or url_for('admin'))
        else:
            flash('Clave incorrecta, por favor intenta de nuevo', 'danger')


    return render_template('admin/login.html', form=form, title='Login Page')