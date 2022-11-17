from flask_app import app, render_template, redirect, request, bcrypt, session, flash
from flask_app.models.user import User
from flask_app.models.question import Question
from flask_app.models.comment import Comment


@app.route('/home')
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/allblogs')
def all_blogs():
    return render_template('all_blogs.html')

# CREATE A Question

@app.route('/community') #! STUDYYYYYYY
def community():
    # GRAB ALL THE QUESTIONS 
    allQuestions = Question.get_all_with_comments()# create a new method get all with questions and comments
    return render_template('community.html', allQuestions = allQuestions)

@app.route("/community/create", methods=['POST'])
def create_question():
    print(request.form)
    if not Question.validate_question(request.form):
        return redirect('/community')
    if "user_id" not in session:
        flash("Register")
        return redirect('/thespot')
    #! This calls on the save model in order to save to the database
    Question.save(request.form)
    return redirect('/community')

@app.route("/community/comment", methods=['POST'])
def create_comment():
    print(request.form)
    # if not Comment.validate_Comment(request.form):
    #     return redirect('/community')
    #! This calls on the save model in order to save to the database
    Comment.save(request.form)
    return redirect('/community')


@app.route('/test')
def test():
    data = {'id': 1}
    Question.get_one_with_comments(data)
    return

#___________________________________________________

@app.route('/access')
def user_access():
    if "user_id" not in session:
        return redirect('/thespot')
    return render_template('access.html')

# Feature

@app.route('/feature')
def feature():
    return render_template('feature.html')

@app.route('/feature2')
def feature2():
    return render_template('feature2.html')

@app.route('/feature3')
def feature3():
    return render_template('feature3.html')

@app.route('/feature4')
def feature4():
    return render_template('feature4.html')










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
