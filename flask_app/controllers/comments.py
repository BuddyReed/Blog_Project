from flask_app import app, render_template, redirect, request, bcrypt, session, flash
from flask_app.models.user import User
from flask_app.models.question import Question



@classmethod
def destory(cls, data):
    query = 'DELETE FROM comments WHERE id = %(id)s'
    return connectToMySQL(DATABASE).query_db(query, data)



# CREATE New Question

# @app.route('/questions/new')
# def new_question():
#     if "user_id" not in session:
#         return redirect('/logout')
#     return render_template('new_questions.html')

# @app.route("/questions/create", methods=['POST'])
# def create_question():
#     print(request.form)
#     if not Question.validate_question(request.form):
#         return redirect('/questions/new')
#     #! This calls on the save model in order to save to the database
#     Question.save(request.form)
#     return redirect('/questions')


# #! This will usually go into a different controller. This is a page after register or login
# @app.route ('/questions')
# def things():
#     if "user_id" not in session:
#         return redirect('/logout')
#     return render_template('questions.html', questions = Question.get_all())

# @app.route('/questions/<int:id>')
# def show_question(id):
#     data = {'id' : id}
#     return render_template('show_question.html', question = Question.get_one(data) )

# #! Update
# @app.route('/questions/edit/<int:id>')
# def edit_question(id):
#     data = {'id' : id}
#     return render_template('edit_question.html', question = Question.get_one(data))

# @app.route('/questions/update', methods=['POST'])
# def update_question():
#     print(request.form)
#     if not Question.validate_question(request.form):
#         return redirect(f"/questions/edit/{request.form['id']} ")
#     Question.update(request.form)
#     return redirect('/questions')

# #! Delete
# @app.route('/questions/delete/<int:id>')
# def delete_question(id):
#     data = {"id" : id}
#     Question.destory(data)
#     return redirect('/questions')
