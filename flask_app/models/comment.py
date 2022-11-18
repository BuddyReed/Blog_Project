from flask_app import flash
from flask_app.config.mysqlconnection import connectToMySQL
import re	# the regex module
# create a regular expression object that we'll use later   
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

DATABASE = 'blog_project'

class Comment:

    def __init__(self, data) -> None:
        self.id = data['id']
        self.content = data['content']
        self.question_id = data['question_id']
        self.user_id = data['user_id'] #! This is a many to many relationship. So you want to access the user id in order to put the many comments.
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user = data['user']
        self.question = data['question']


    #! Create
    @classmethod
    def save(cls, data):
        query = "INSERT INTO comments (content, user_id, question_id) VALUES (%(content)s, %(user_id)s, %(question_id)s)"
        result = connectToMySQL(DATABASE).query_db(query, data)
        return result


    #! This method shows all the user comments on the comments page.. 
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM comments JOIN users ON users.id = comments.user_id;"
        # make sure to call the connectToMySQL function with the schema you are targeting. WHICH MAKES A LIST OF DICTONIERS
        results = connectToMySQL(DATABASE).query_db(query)
        # Create an empty list to append our instances (NEW commentS) of comments
        comments = []
        # Iterate over the db results and create instances of comments with cls.
        for comment in results:
            comments.append( cls(comment) )
        return comments
    
    # Read one and adding the one to many relationship 
    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM comments JOIN users ON users.id = comments.user_id WHERE comments.id = %(id)s;" #! STUDYYYY
        result =  connectToMySQL(DATABASE).query_db(query, data) 
        return cls(result[0])
    
    @staticmethod
    def validate_comment(comment):
        print(type(comment['content']))
        is_valid = True 
        if len(comment['content']) < 1:
            flash('Comment must be at least  chararacters')
            is_valid = False
        return is_valid

    @classmethod
    def get_comment_with_user(cls, data):
        query = "SELECT * FROM comments LEFT JOIN users ON comments.user_id = users.id WHERE comments.id = %(id)s;"
        results = connectToMySQL(DATABASE).query_db(query, data)
        comment_data = {
            'id': results[0]['id'],
            'content': results[0]['content']
        }
        comment =  Comment(results[0])
    
    #!UPDATE
    @classmethod
    def update(cls, data):
        query = "UPDATE comments SET title=%(title)s, description=%(description)s, price=%(price)s, user_id=%(user_id)s WHERE id= %(id)s"
        return connectToMySQL(DATABASE).query_db(query, data) 

    @classmethod
    def destory(cls, data):
        query = 'DELETE FROM comments WHERE id = %(id)s'
        return connectToMySQL(DATABASE).query_db(query, data)