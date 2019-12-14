import re
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, Regexp, URL


from flask_app.models import Listing


class CreateForm(FlaskForm):
    item_name = StringField('Item Name', validators=[DataRequired(), Length(min=2, max=30)])
    item_desc = TextAreaField('Item Description', validators=[DataRequired(), Length(min=10,max=300)])
    price = StringField('Price $ *include shipping', validators=[DataRequired(), Regexp(re.compile('^[+-]?[0-9]{1,3}(?:,?[0-9]{3})*\.[0-9]{2}$'))])
    item_picture_url = StringField('Image URL', validators=[DataRequired(), URL()])
    submit = SubmitField('Sell Item')

