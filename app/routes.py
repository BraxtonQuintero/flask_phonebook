from flask import render_template, redirect, url_for, flash
from app import app
from app.forms import SignUpForm

@app.route("/")
def base():
    return render_template('base.html')

@app.route("/signup", methods = ["GET", "POST"])
def sign_up():
    user_form = SignUpForm()
    if user_form.validate_on_submit():
        print("Congrats You Submitted Your Info!")
        first = user_form.first_name.data
        last = user_form.last_name.data
        phone_number = user_form.phone_number.data
        address = user_form.address.data
        print(first, last, phone_number, address)
        flash("Your Info Has Been Saved")
        return redirect(url_for('base'))

    return render_template('signup.html', user_form = user_form)