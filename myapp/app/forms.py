from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length

class ItemForm(FlaskForm):
    title = StringField('Название', 
                       validators=[DataRequired(), 
                                 Length(min=2, max=100)])
    description = TextAreaField('Описание', 
                              validators=[Length(max=500)])
    submit = SubmitField('Сохранить')