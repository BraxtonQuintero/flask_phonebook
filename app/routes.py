from flask import render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user, login_required
from app import app
from app.forms import SignUpForm, LogInForm, Addcontact
from app.models import User, Addcontact

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
        username = form.username.data
        password = form.password.data
        print(first, last, username, password)
        
        check_user = User.query.filter( (User.username == username) | (User.password == password) ).first()
        if check_user is not None:
            flash('Phone Number and/or already in you Phone Book', 'danger')
            return redirect(url_for('signup'))

        new_user = User(first_name=first, last_name=last, username=username, password=password)

        flash(f"{new_user} has successfully signed up!", "success")

        return redirect(url_for('index'))

    return render_template('signup.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LogInForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = User.query.filter_by(username=username).first()
        if user is not None and user.check_password(password):
            login_user(user)
            flash(f"{user} is now logged in.", 'primary')
            return redirect(url_for('index'))
        else:
            flash('Incorrect username and/or password. Please try again.', 'danger')
            return redirect(url_for('login'))

    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out', 'info')
    return redirect(url_for('index'))


@app.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    form = Addcontact()
    if form.validate_on_submit():
        first = form.first_name.data
        last = form.last_name.data
        phone = form.phone_number.data
        address = form.address.data
        new_post = Addcontact(first_name=first, last_name=last, phone_number=phone, address=address, user_id=current_user.id)

        flash(f"{new_post.first} has been created.", "success")

        return redirect(url_for('index'))

    return render_template('create.html', form=form)

@app.route('/posts/<post_id>')
def get_post(post_id):
    post = Addcontact.query.get(post_id)
    if not post:
        flash(f"Post with id #{post_id} does not exist", "warning")
        return redirect(url_for('index'))
    return render_template('post.html', post=post)

@app.route('/posts/<post_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_post(post_id):
    post = Addcontact.query.get(post_id)
    if not post:
        flash(f"Post with id #{post_id} does not exist", "warning")
        return redirect(url_for('index'))
    if post.author != current_user:
        flash('You do not have permission to edit this post', 'danger')
        return redirect(url_for('index'))
    form = Addcontact()
    if form.validate_on_submit():
        new_first = form.first_name.data
        new_last = form.last_name.data
        new_phone = form.phone_number.data
        new_address = form.address.data
        post.update(first_name=new_first, last_name=new_last,phone_number=new_phone,address=new_address)
        flash(f"{post.first} has been updated", "success")
        return redirect(url_for('get_post', post_id=post.id))
    return render_template('edit_post.html', post=post, form=form)

@app.route('/posts/<post_id>/delete')
@login_required
def delete_post(post_id):
    post = Addcontact.query.get(post_id)
    if not post:
        flash(f"Post with id #{post_id} does not exist", "warning")
        return redirect(url_for('index'))
    if post.author != current_user:
        flash('You do not have permission to delete this post', 'danger')
        return redirect(url_for('index'))
    post.delete()
    flash(f"{post.title} has been deleted", 'info')
    return redirect(url_for('index'))