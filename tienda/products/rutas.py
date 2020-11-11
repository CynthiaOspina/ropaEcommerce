from flask import redirect, render_template, url_for, flash, request, session, current_app
from app import db, app, photos, search
from .models import Brand, Category, Product
from .forms import addproducts
from tienda.admin.rutas import brandsF, categories
import secrets, os

@app.route('/result')
def result():
    searchword = request.args.get('q')
    products = Product.query.msearch(searchword, fields=['name', 'desc'], limit=6)
    return render_template('products/result.html', products=products, brands=brandsF(), categories=categories())

@app.route('/addbrand', methods=['GET','POST'])
def addbrand():
    if request.method == "POST":
        getbrand = request.form.get('brand')
        brand = Brand(name=getbrand)
        db.session.add(brand)
        flash(f'La marca {getbrand} fue añadida a su base de datos','success')
        db.session.commit()
        return redirect(url_for('addbrand'))
    return render_template('products/addbrand.html', brands='brands')

@app.route('/updatebrand/<int:id>', methods=['GET','POST'])
def updatebrand(id):
    if 'email' not in session:
        flash(f'Porfavor ingrese primero','danger')
        return redirect(url_for('login'))
    updatebrand = Brand.query.get_or_404(id)
    brand = request.form.get('brand')
    if request.method == 'POST':
        updatebrand.name = brand
        flash(f'Su marca ha sido actualizada','success')
        db.session.commit()
        return redirect(url_for('brands'))
    return render_template('products/updatebrand.html', title='Actualizar Marca', updatebrand=updatebrand)

@app.route('/deletebrand/<int:id>', methods=['GET','POST'])
def deletebrand(id):
    if 'email' not in session:
        flash(f'Porfavor ingrese primero','danger')
        return redirect(url_for('login'))
    brand = Brand.query.get_or_404(id)
    if request.method == 'POST':
        db.session.delete(brand)
        db.session.commit()
        flash(f'Su marca: {brand.name} ha sido eliminada de la base de datos','success')
        return redirect(url_for('brands'))
    flash(f'Su marca {brand.name} no se pudo eliminar','warning')
    return render_template('products/updatebrand.html')

@app.route('/updatecat/<int:id>', methods=['POST','GET'])
def updatecategory(id):
    if 'email' not in session:
        flash(f'Porfavor ingrese primero','danger')
        return redirect(url_for('login'))
    updatecategory = Category.query.get_or_404(id)
    category = request.form.get('category')
    if request.method == 'POST':
        updatecategory.name = category
        flash(f'Su categoria ha sido actualizada', 'success')
        db.session.commit()
        return redirect(url_for('category'))
    return render_template('products/updatebrand.html', title='Actualizar Categoria', updatecategory=updatecategory)

@app.route('/addcat', methods=['GET','POST'])
def addcat():
    if request.method == "POST":
        getCategory = request.form.get('category')
        category = Category(name=getCategory)
        db.session.add(category)
        flash(f'La marca {getCategory} fue añadida a su base de datos','success')
        db.session.commit()
        return redirect(url_for('addcat'))
    return render_template('products/addbrand.html')

@app.route('/deletecat/<int:id>', methods=['GET','POST'])
def deletecat(id):
    if 'email' not in session:
        flash(f'Porfavor ingrese primero','danger')
        return redirect(url_for('login'))
    cat = Category.query.get_or_404(id)
    if request.method == 'POST':
        db.session.delete(cat)
        db.session.commit()
        flash(f'Su categoria: {cat.name} ha sido eliminada de la base de datos','success')
        return redirect(url_for('category'))
    flash(f'Su marca {cat.name} no se pudo eliminar','warning')
    return render_template('products/updatebrand.html')

@app.route('/addproduct', methods=['POST','GET'])
def addproduct():
    brands = Brand.query.all()
    categories = Category.query.all()
    form = addproducts(request.form)
    if request.method == 'POST':
        name= form.name.data
        price = form.price.data
        discount = form.discount.data
        stock = form.stock.data
        colors = form.color.data
        desc = form.description.data
        brand = request.form.get('brand')
        category = request.form.get('category')
        image_1 = photos.save(request.files.get('image_1'), name=secrets.token_hex(10) + ".")
        image_2 = photos.save(request.files.get('image_2'), name=secrets.token_hex(10) + ".")
        image_3 = photos.save(request.files.get('image_3'), name=secrets.token_hex(10) + ".")

        addpro = Product(name=name, price=price, discount=discount, stock=stock, colors=colors, desc=desc, brand_id=brand, category_id=category, image_1=image_1, image_2=image_2, image_3=image_3)
        db.session.add(addpro)
        flash(f'El producto {name} ha sido añadido a la base de datos', 'success')
        db.session.commit()
        return redirect(url_for('admin'))


    return render_template('products/addproduct.html', title='Página Añadir Productos', form=form, brands=brands, categories=categories)

@app.route('/updateproduct/<int:id>', methods=['POST','GET'])
def updateproduct(id):
    brands = Brand.query.all()
    categories = Category.query.all()
    product = Product.query.get_or_404(id)
    brand = request.form.get('brand')
    category = request.form.get('category')
    form = addproducts(request.form)
    if request.method == 'POST':
        product.name = form.name.data
        product.price = form.price.data
        product.discount = form.discount.data
        product.brand_id = brand
        product.category_id = category
        product.colors = form.color.data
        product.stock = form.stock.data
        product.desc = form.description.data
        if request.files.get('image_1'):
            try:
                os.unlink(os.path.join(current_app.root_path, "static/images/" + product.image_1))
                product.image_1 = photos.save(request.files.get('image_1'), name=secrets.token_hex(10) + ".")
            except:
                product.image_1 = photos.save(request.files.get('image_1'), name=secrets.token_hex(10) + ".")

        if request.files.get('image_2'):
            try:
                os.unlink(os.path.join(current_app.root_path, "static/images/" + product.image_2))
                product.image_2 = photos.save(request.files.get('image_2'), name=secrets.token_hex(10) + ".")
            except:
                product.image_2 = photos.save(request.files.get('image_2'), name=secrets.token_hex(10) + ".")

        if request.files.get('image_3'):
            try:
                os.unlink(os.path.join(current_app.root_path, "static/images/" + product.image_3))
                product.image_3 = photos.save(request.files.get('image_3'), name=secrets.token_hex(10) + ".")
            except:
                product.image_3 = photos.save(request.files.get('image_3'), name=secrets.token_hex(10) + ".")

        db.session.commit()
        flash(f'El product ha sido actualizado', 'success')
        return redirect(url_for('admin'))

    form.name.data = product.name
    form.price.data = product.price
    form.discount.data = product.discount
    form.stock.data = product.stock
    form.color.data = product.colors
    form.description.data = product.desc


    return render_template('products/updateproduct.html', title='Actualizar Producto', form=form, categories=categories, brands=brands, product=product)

@app.route('/deleteproduct/<int:id>', methods=['GET','POST'])
def deleteproduct(id):
    product = Product.query.get_or_404(id)
    if request.method == 'POST':
        try:
            os.unlink(os.path.join(current_app.root_path, "static/images/" + product.image_1))
            os.unlink(os.path.join(current_app.root_path, "static/images/" + product.image_2))
            os.unlink(os.path.join(current_app.root_path, "static/images/" + product.image_3))
        except Exception as e:
            print(e)

        db.session.delete(product)
        db.session.commit()
        flash(f'Su producto: {product.name} ha sido eliminado de la base de datos','success')
        return redirect(url_for('admin'))
    flash(f'Su producto {product.name} no se pudo eliminar','warning')
    return render_template('admin/index.html')