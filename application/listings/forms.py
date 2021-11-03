from flask import request
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, IntegerField, FloatField, TextAreaField, FileField, SubmitField
from wtforms.validators import DataRequired, Optional, ValidationError
from wtforms.widgets.html5 import NumberInput


class ListingForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired()])
    beds = IntegerField('Beds', widget=NumberInput(min=1), validators=[DataRequired()])
    baths = IntegerField('Baths', widget=NumberInput(min=1), validators=[DataRequired()])
    price = FloatField('Price', widget=NumberInput(min=1, step=0.01), validators=[DataRequired()])
    description = TextAreaField('Description', validators=[Optional()])
    picture = FileField('Upload Picture', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])

    submit = SubmitField('List')


class SearchForm(FlaskForm):
    q = StringField(('Search'), validators=[DataRequired()])

    def __init__(self, *args, **kwargs):
        if 'formdata' not in kwargs:
            kwargs['formdata'] = request.args
        if 'csrf_enabled' not in kwargs:
            kwargs['csrf_enabled'] = False
        super(SearchForm, self).__init__(*args, **kwargs)


class SpecificSearchForm(FlaskForm):
    beds = IntegerField('Beds', widget=NumberInput(min=1), validators=[DataRequired()])
    baths = IntegerField('Baths', widget=NumberInput(min=1), validators=[DataRequired()])
    minprice = FloatField('Min Price', widget=NumberInput(min=1, step=0.01), validators=[DataRequired()])
    maxprice = FloatField('Min Price', widget=NumberInput(min=1, step=0.01), validators=[DataRequired()])

    submit = SubmitField('Search')
            