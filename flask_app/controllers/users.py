from flask_app import app, render_template, redirect, request, bcrypt, session, flash
from flask_app.models.user import User

@app.route('/thespot')
def index():
    return render_template('index.html')

#! Create aka Register

@app.route('/register', methods = ['post'])
def register():
    print(request.form)
    # TODO VALIDATE OUR USER
    if not User.validate_user(request.form):
        return redirect('/thespot')
    # TODO check to see if the email supplied is already in our DB
    data = {'email': request.form['email']}
    check_for_user = User.get_by_email(data)
    if check_for_user:
        flash("email already registered")
        return redirect('/thespot')
    # TODO HASH THE PASSWORD
    hashed_pw = bcrypt.generate_password_hash(request.form['password'])
    # TODO SAVE USER TO THE DATABASE
    user_data = {
        'first_name' : request.form['first_name'],
        'last_name' : request.form['last_name'],
        'email' : request.form['email'],
        'password' : hashed_pw
    }
    user_id = User.save(user_data)
    # TODO LOG IN USER
    session['user_id'] = user_id
    session['first_name'] = request.form['first_name']
    session['last_name'] = request.form['last_name']

    return redirect('/access')
    

#! Read and Verfy AKA Login
@app.route('/login', methods=['POST'])
def login():
    # TODO see if the email is in our DB
    print(request.form)
    user = User.get_by_email(request.form)
    if not user:
        flash("Invalid credentials")
        return redirect('/thespot')
    # TODO check to see if password matches what is in the DB
    password_valid = bcrypt.check_password_hash(user.password, request.form['password'])
    print(user)
    if not password_valid:
        flash('Invalid credentials')
        return redirect('/thespot')
    # TODO log in user
    session['user_id'] = user.id
    session['first_name'] = user.first_name
    return redirect('/access')

#____________________________________________

#! Logout

@app.route('/logout')
def logout():
    session.clear()
    print(session)
    return redirect('/')