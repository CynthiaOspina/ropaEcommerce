from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_uploads import IMAGES, UploadSet, configure_uploads, patch_request_class
import os
from flask_msearch import Search
from flask_login import LoginManager
from flask_migrate import Migrate

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://rsuodfqr:haY5De1RVPHsZ_obWfkZi9fBJY_vNwQJ@lallah.db.elephantsql.com:5432/rsuodfqr'
app.config['SECRET_KEY'] = 'owjADSFe4wqjfqwfe324'
app.config['UPLOADED_PHOTOS_DEST'] = os.path.join(basedir, 'static/images')

photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)
patch_request_class(app)

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
search = Search()
search.init_app(app)

migrate = Migrate(app, db)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view='customerLogin'
login_manager.needs_refresh_message_category='danger'
login_manager.login_message = u"Por favor, ingrese primero"

from tienda.admin import rutas
from tienda.products import rutas
from tienda.carts import carts
from tienda.cliente import rutas


if __name__ == '__main__':
    app.run()
