from flask import Blueprint, render_template, redirect, url_for, request, flash, Response
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from .models import User
from . import db, current_time, book_time, get_time
from .models import Book

auth = Blueprint('auth', __name__)


@auth.route('/book')
@login_required
def book():
    books = Book.query.filter_by(status=0).all()
    checks = Book.query.filter_by(plate=current_user.plate).all()
    booked = False
    if checks:
        for check in checks:
            if check.exptime > current_time():
                booked = True
    slots = []
    for book in books:
        if int(book.exptime) < current_time():
            slots.append(book.slot)
    if len(slots) == 0:
        empty = True
    else:
        empty = False
    return render_template('book.html', slots=slots, empty=empty, booked=booked)


@auth.route('/profile')
@login_required
def profile():
    checks = Book.query.filter_by(plate=current_user.plate).all()
    booked = False
    allocated = False
    slot = ''
    m = 0
    s = 0
    if checks:
        for check in checks:
            if check.exptime > current_time():
                booked = True
                slot = check.slot
                m, s = get_time(str(check.exptime))
                if int(check.status) != 0:
                    allocated = True
    return render_template('profile.html', name=current_user.name,
            plate=current_user.plate, booked=booked,
            allocated=allocated,
            slot=slot, min=m, sec=s)


@auth.route('/book', methods=['POST'])
@login_required
def book_post():
    slot = request.form.get('slot')
    print(slot)
    book = Book.query.filter_by(slot=slot).first()
    book.plate = current_user.plate
    book.exptime = book_time()
    db.session.commit()
    return redirect(url_for('main.profile'))


@auth.route('/login')
def login():
    return render_template('login.html')


@auth.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.')
        return redirect(url_for('auth.login'))

    login_user(user, remember=remember)

    return redirect(url_for('main.profile'))


@auth.route('/signup')
def signup():
    return render_template('signup.html')


@auth.route('/signup', methods=['POST'])
def signup_post():
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')
    plate = request.form.get('plate')
    subexp = request.form.get('subexp')

    user = User.query.filter_by(email=email).first()

    if user:
        flash('Email address already exists.')
        return redirect(url_for('auth.signup'))

    new_user = User(email=email, name=name, password=generate_password_hash(password, method='sha256'),
                    plate=plate, subexp=subexp)

    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('auth.login'))


@auth.route('/changepwd')
def changepwd():
    return render_template('changepwd.html')


@auth.route('/changepwd', methods=['POST'])
def changepwd_post():
    oldpwd = request.form.get('oldpwd')
    newpwd = request.form.get('newpwd')
    confirmpwd = request.form.get('confirmpwd')

    user = User.query.filter_by(email=current_user.email).first()

    if not check_password_hash(user.password, oldpwd):
        flash('Wrong Password')
        return redirect(url_for('auth.changepwd'))

    elif confirmpwd != newpwd:
        flash('Passwords Does not Match.')
        return redirect(url_for('auth.changepwd'))

    elif check_password_hash(user.password, newpwd):
        flash('You wrote old password.')
        return redirect(url_for('auth.changepwd'))

    user.password = generate_password_hash(newpwd, method='sha256')
    db.session.commit()

    return redirect(url_for('main.profile'))


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))


@auth.route('/update_slot', methods=['GET', 'POST'])
def update_slot():
    if request.remote_addr == '127.0.0.1':
        data = request.json
        for key, value in data.items():
            slot = Book.query.filter_by(slot=key).first()
            print("Key: {}, Value: {}".format(key, value))
            slot.status = int(value)
            print(slot.status)
        print(data)
        db.session.commit()

        return Response("OK", status=200, mimetype='application/json')
    else:
        return Response("ERROR", status=403, mimetype='application/json')


@auth.route('/get_plate', methods=['GET', 'POST'])
def get_plate():
    print(request.remote_addr)
    if request.remote_addr == '127.0.0.1':
        data = request.json
        print(data)

        booked = False
        for r in data["results"]:
            checks = Book.query.filter_by(plate=r).all()
            if checks:
                for check in checks:
                    if check.exptime > current_time():
                        booked = True
        if booked:
            return Response("OK", status=200, mimetype='application/json')
        else:
            return Response("ERROR", status=403, mimetype='application/json')
    else:
        return Response("ERROR", status=403, mimetype='application/json')
