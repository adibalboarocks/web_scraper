from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError
from master.models import User
from wtforms import SelectMultipleField, DateField, SubmitField
from wtforms.validators import DataRequired 
from wtforms.widgets import ListWidget, CheckboxInput
from datetime import date
from flask import flash
from datetime import date, timedelta, datetime



class RegisterForm(FlaskForm):
    def validate_username(self, username_to_check):
        user = User.query.filter_by(username=username_to_check.data).first()
        if user:
            raise ValidationError('Username already exists! Please try a different username')

    def validate_email_address(self, email_address_to_check):
        email_address = User.query.filter_by(email_address=email_address_to_check.data).first()
        if email_address:
            raise ValidationError('Email Address already exists! Please try a different email address')

    username = StringField(label='User Name:', validators=[Length(min=2, max=30), DataRequired()])
    email_address = StringField(label='Email Address:', validators=[Email(), DataRequired()])
    password1 = PasswordField(label='Password:', validators=[Length(min=6), DataRequired()])
    password2 = PasswordField(label='Confirm Password:', validators=[EqualTo('password1'), DataRequired()])
    submit = SubmitField(label='Create Account')



class LoginForm(FlaskForm):
    username = StringField(label='User Name:', validators=[DataRequired()])
    password = PasswordField(label='Password:', validators=[DataRequired()])
    submit = SubmitField(label='Sign in')



class MultiCheckboxField(SelectMultipleField):
    widget = ListWidget(prefix_label=False)
    option_widget = CheckboxInput()


class MyForm(FlaskForm):
    choices = [('option1', 'Telecoms.com'), ('option2', 'telecomramblings.com')]
    multiple_choices = MultiCheckboxField('Multiple Choices', choices=choices)
    date1 = DateField('Start Date', validators=[DataRequired()])
    date2 = DateField('End Date', validators=[DataRequired()])

    def validate(self,extra_validators=None):
        if not super().validate():
            return False
        
        if self.date1.data > self.date2.data:
            flash('Start date must be before End date.', category='danger')
            return False
        
        disabled_start_date = date.today() + timedelta(days=1)  # Start date of disabled range (date after today)

        if disabled_start_date <= self.date1.data or disabled_start_date <= self.date2.data:
            flash('Make sure both dates are not a future date', category='danger')
            return False
        
        return True
    
class NewForm(FlaskForm):
    checkbox_field = MultiCheckboxField(choices=[('option1', 'telecomstechnews.com'), ('option2', 'telecomtalk.info')])
    submit = SubmitField('Scrape home page')