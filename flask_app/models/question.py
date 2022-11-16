from flask_app import flash
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.comment import Comment
from pprint import pprint
from flask_app.models.user import User
import re	# the regex module
# create a regular expression object that we'll use later   
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

DATABASE = 'blog_project'

class Question:

    def __init__(self, data) -> None:
        self.id = data['id']
        self.content = data['content']
        self.user_id = data['user_id'] #! This is a many to many relationship. So you want to access the user id in order to put the many questions.
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user = data['user']
        self.comments = []


    #! Create
    @classmethod
    def save(cls, data):
        query = "INSERT INTO questions (content, user_id) VALUES (%(content)s, %(user_id)s)"
        result = connectToMySQL(DATABASE).query_db(query, data)
        return result


    #! This method shows all the user questions on the questions page.. 
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM questions JOIN users ON users.id = questions.user_id;"
        # make sure to call the connectToMySQL function with the schema you are targeting. WHICH MAKES A LIST OF DICTONIERS
        results = connectToMySQL(DATABASE).query_db(query)
        # Create an empty list to append our instances (NEW questionS) of questions
        questions = []
        # Iterate over the db results and create instances of questions with cls.
        for question in results:
            questions.append( cls(question) )
        return questions
    
    @classmethod
    def get_all_with_comments(cls):
        query = "SELECT id FROM questions;"
        questions = []
        question_ids = connectToMySQL(DATABASE).query_db(query)
        for id in question_ids:
            questions.append(cls.get_one_with_comments(id))
        return questions
    
    # Read one and adding the one to many relationship 
    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM questions JOIN users ON users.id = questions.user_id WHERE questions.id = %(id)s;" #! STUDYYYY
        result =  connectToMySQL(DATABASE).query_db(query, data) 
        return cls(result[0])
    
    @classmethod
    def get_one_with_comments(cls, data):
        query = "SELECT * FROM questions LEFT JOIN users ON users.id = questions.user_id LEFT JOIN comments ON comments.question_id = questions.id WHERE questions.id = %(id)s;" #! STUDYYYY
        results =  connectToMySQL(DATABASE).query_db(query, data)
        pprint(results)
        user_data = {
            'id': results[0]['user_id']
        }
        user = User.get_by_id(user_data)
        question_data = {
            'id': results[0]['id'],
            'content': results[0]['content'],
            'user_id': results[0]['user_id'],
            'created_at': results[0]['created_at'],
            'updated_at': results[0]['updated_at'],
            'user': user,
        }
        question = Question(question_data)
        
        question.user = user
        for comment in results:
            comment_user_data = {
                'id': comment['comments.user_id']
            }
            comment_user = User.get_by_id(comment_user_data)
            comment_data = {
                'id': comment['comments.id'],
                'content': comment['comments.content'],
                'question_id': comment['question_id'],
                'user_id': comment['comments.user_id'],
                'created_at': comment['comments.created_at'],
                'updated_at': comment['comments.updated_at'],
                'user': comment_user,
                'question': question,
            }
            question.comments.append(Comment(comment_data))
        return question
    
    # Read one Question and Get All comments
    
    @classmethod
    def get_one_with_questions(cls, data):
        query = "SELECT * FROM comments LEFT JOIN questions ON comments.id = questions.comment_id WHERE comments.id = %(id)s;"
        results =  connectToMySQL(DATABASE).query_db(query, data) 
        print(results)
        comment = Comment(results[0])
        print(comment.name)
        for result in results:
            temp_question = {
                'id' : result['questions.id'],
                'content' : result['content'],
                'comment_id' : result['comment_id'],
                'created_at' : result['created_at'],
                'updated_at' : result['updated_at'],
            }
            comment.questions.append(Question(temp_question))
        return comment
    
    
    
    
    @staticmethod
    def validate_question(question):
        print(type(question['content']))
        is_valid = True 
        if len(question['content']) < 10:
            flash('Description must be at least 3 chararacters')
            is_valid = False
        return is_valid
    
    #!UPDATE
    @classmethod
    def update(cls, data):
        query = "UPDATE questions SET title=%(title)s, description=%(description)s, price=%(price)s, user_id=%(user_id)s WHERE id= %(id)s"
        return connectToMySQL(DATABASE).query_db(query, data) 

    @classmethod
    def destory(cls, data):
        query = 'DELETE FROM questions WHERE id = %(id)s'
        return connectToMySQL(DATABASE).query_db(query, data)