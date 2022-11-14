from flask_app import app, render_template, redirect, request, bcrypt, session, flash
from flask_app.models.user import User
from flask_app.models.painting import Painting


@app.route('/home')
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/allblogs')
def all_blogs():
    return render_template('all_blogs.html')

@app.route('/feature')
def feature():
    return render_template('feature.html')

@app.route('/community')
def community():
    return render_template('community.html')

@app.route('/access')
def user_access():
    return render_template('access.html')




# CREATE New Painting

# @app.route('/paintings/new')
# def new_painting():
#     if "user_id" not in session:
#         return redirect('/logout')
#     return render_template('new_paintings.html')

# @app.route("/paintings/create", methods=['POST'])
# def create_painting():
#     print(request.form)
#     if not Painting.validate_painting(request.form):
#         return redirect('/paintings/new')
#     #! This calls on the save model in order to save to the database
#     Painting.save(request.form)
#     return redirect('/paintings')


# #! This will usually go into a different controller. This is a page after register or login
# @app.route ('/paintings')
# def things():
#     if "user_id" not in session:
#         return redirect('/logout')
#     return render_template('paintings.html', paintings = Painting.get_all())

# @app.route('/paintings/<int:id>')
# def show_painting(id):
#     data = {'id' : id}
#     return render_template('show_painting.html', painting = Painting.get_one(data) )

# #! Update
# @app.route('/paintings/edit/<int:id>')
# def edit_painting(id):
#     data = {'id' : id}
#     return render_template('edit_painting.html', painting = Painting.get_one(data))

# @app.route('/paintings/update', methods=['POST'])
# def update_painting():
#     print(request.form)
#     if not Painting.validate_painting(request.form):
#         return redirect(f"/paintings/edit/{request.form['id']} ")
#     Painting.update(request.form)
#     return redirect('/paintings')

# #! Delete
# @app.route('/paintings/delete/<int:id>')
# def delete_painting(id):
#     data = {"id" : id}
#     Painting.destory(data)
#     return redirect('/paintings')
