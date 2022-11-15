from flask_app import flash
from flask_app.config.mysqlconnection import connectToMySQL
import re	# the regex module
# create a regular expression object that we'll use later   
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

DATABASE = 'blog_project'

class Question:

    def __init__(self, data) -> None:
        self.id = data['id']
        self.content = data['content']
        self.user_id = data['user_id'] #! This is a many to many relationship. So you want to access the user id in order to put the many questions.
        self.first_name = data['first_name'] # Adding this allows you to show the who the question was posted by. Also referenec the query in get all.
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']


    #! Create
    @classmethod
    def save(cls, data):
        query = "INSERT INTO questions (title, description, price, user_id) VALUES (%(title)s, %(description)s, %(price)s, %(user_id)s)"
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
    
    # Read one and adding the one to many relationship 
    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM questions JOIN users ON users.id = questions.user_id WHERE questions.id = %(id)s;" #! STUDYYYY
        result =  connectToMySQL(DATABASE).query_db(query, data) 
        return cls(result[0])
    
    @staticmethod
    def validate_question(question):
        print(type(question['price']))
        is_valid = True 
        if len(question['description']) < 10:
            flash('Description must be at least 3 chararacters')
            is_valid = False
        if len(question['title']) < 2:
            flash('Title must be at least 2 chararacters')
            is_valid = False
        if  not question['price']:
            flash('Please Enter Price')
            is_valid = False
        if  question['price'] and int((question['price'])) <= 0:
            print(type(question['price']))
            flash('Price must be at great than $0')
            is_valid = False
            #! ADDDDDD PRICE
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