from master import app, scrape, storing
from flask import render_template,request, redirect, url_for, flash, session, send_file, make_response
import pandas as pd
from master.forms import MyForm,NewForm
from master.forms import RegisterForm, LoginForm, MultiCheckboxField
from master.models import db,User
from flask_login import login_user,logout_user, current_user
import json 
from datetime import datetime, date, timedelta
from pymongo import MongoClient
import os 

@app.route('/')
def intro_page():
    return render_template('intro.html')

@app.route('/home', methods=['GET', 'POST'])
def base_page():
    session['selected_choices'] = None
    session['date1'] = None
    session['date2'] = None
    session['selected_options']=None
    form = MyForm()
    if form.validate_on_submit(extra_validators=None):
        # Process the form data
        selected_choices = form.multiple_choices.data
        date1 = form.date1.data
        date2 = form.date2.data
        session['selected_choices'] = selected_choices
        session['date1'] = date1
        session['date2'] = date2

        if date1 > date2:
            flash('Start date must be before End date.', category='danger')
        elif date1 > date.today() or date2 > date.today():
            flash('Make sure both dates are not a future date', category='danger')
        else:
            # Redirect to the new route
            return redirect(url_for('upload'))
    
        
    form2 = NewForm()
    if form2.validate_on_submit():
        selected_options = form2.checkbox_field.data
        session['selected_options']=selected_options
        return redirect(url_for('upload'))

    return render_template('base.html', form=form, form2=form2)

@app.route('/upload',methods=['GET','POST'])
def upload():
    date1=session.get('date1')    
    date2=session.get('date2')
    selected_choices=session.get('selected_choices') 
    selected_options=session.get('selected_options') 
    full_dict=scrape.router(date1,date2,selected_choices,selected_options)
    if current_user.is_authenticated: storing.store(current_user.username,current_user.email_address,full_dict)
    df = pd.DataFrame(full_dict)
    #Generate HTML table from DataFrame
    table= df.to_html(index=False)
    return render_template('result.html',table=table)




@app.route('/register', methods=['GET', 'POST'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(username=form.username.data,
                              email_address=form.email_address.data,
                              password=form.password1.data)
        db.session.add(user_to_create)
        db.session.commit()
        return redirect(url_for('base_page'))
    if form.errors != {}: #If there are not errors from the validations
        for err_msg in form.errors.values():
            flash(f'There was an error with creating a user: {err_msg}', category='danger')

    return render_template('register.html', form=form)



@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user=User.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(attempted_password=form.password.data):
                login_user(attempted_user)
                flash( f'Success! you are logged in as {attempted_user.username}', category='success')
                return redirect(url_for('base_page'))
        else: flash( f'Username and password are not a match',category='danger')

    return render_template('login.html', form=form)



@app.route('/logout')
def logout_page():
    logout_user()
    flash("You have been logged out!", category='info')
    return redirect(url_for("base_page"))

@app.route('/records')
def record():
    client = MongoClient('mongodb://localhost:27017/')
    db = client['Scraped_data']
    collection = db['user_log']
    documents = collection.find({"username":current_user.username}).sort("_id",-1)  
    return render_template('record.html', documents=documents)

@app.route('/singular/<variable>')
def single_record(variable):
    client = MongoClient('mongodb://localhost:27017/')
    db = client['Scraped_data']
    collection = db[current_user.username]
    print(type(variable))
    documents = collection.find_one({"_id":variable}) 
    return render_template('single_record.html', documents=documents)