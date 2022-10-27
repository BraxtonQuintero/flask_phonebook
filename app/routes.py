from flask import render_template, redirect, url_for, flash
from flask_login import login_user, logout_user
from app import app
from app.forms import SignUpForm, LogInForm
from app.models import User

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signup', methods=["GET", "POST"])
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
        print('Hooray your profile has been submitted!')
        first = form.first_name.data
        last = form.last_name.data
        phone = form.phone_number.data
        home = form.address.data
        print(first, last, phone, home)
        
        check_user = User.query.filter( (User.first_name == first) | (User.phone_number == phone) ).first()
        if check_user is not None:
            flash('Phone Number and/or already in you Phone Book', 'danger')
            return redirect(url_for('signup'))

        new_user = User(first_name=first, last_name=last, phone_number=phone, address = home)

        flash(f"{new_user} has successfully signed up!", "success")

        return redirect(url_for('index'))

    return render_template('signup.html', form=form)