from flask_wtf.file import FileAllowed, FileField, FileRequired
from wtforms import Form, IntegerField, StringField, BooleanField, TextAreaField, validators, DecimalField

class addproducts(Form):
    name = StringField('Nombre', [validators.DataRequired()])
    price = DecimalField('Precio', [validators.DataRequired()])
    discount = IntegerField('Descuento', default=0)
    stock = IntegerField('Cantidad', [validators.DataRequired()])
    description = TextAreaField('Descripción', [validators.DataRequired()])
    color = TextAreaField('Colores', [validators.DataRequired()])
    image_1 = FileField('Imagen 1', validators=[FileAllowed(['jpg','png','jpeg','gif'])])
    image_2 = FileField('Imagen 2', validators=[FileAllowed(['jpg','png','jpeg','gif'])])
    image_3 = FileField('Imagen 3', validators=[FileAllowed(['jpg','png','jpeg','gif'])])