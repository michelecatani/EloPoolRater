from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError
from rankTheBoysApp.models import Pool

class CreatePoolForm(FlaskForm):
    poolname = StringField('PoolName', validators=[DataRequired(), Length(min=2, max=20)])
    submit = SubmitField('Create')

    def validate_poolname(self, poolname):
        ## if there is a value, it'll be here. if not, it will jsut return none
        poolname = Pool.query.filter_by(name=poolname.data).first()
        ## if user is none, won't hit this conditional
        if poolname:
            raise ValidationError('A pool with that name has already been created!')

class JoinPoolForm(FlaskForm):
    poolname = StringField('PoolName', validators=[DataRequired(), Length(min=2, max=20)])
    search = SubmitField('Search')
    
    def validate_pool(self, poolname):
        poolname = Pool.query.filter_by(name=poolname.data).first()
        if not poolname:
            raise ValidationError('That pool doesn\'t exist!')