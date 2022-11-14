from flask_app import flash
from flask_app.config.mysqlconnection import connectToMySQL
import re	# the regex module
# create a regular expression object that we'll use later   
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

DATABASE = 'paintings'

class Painting:

    def __init__(self, data) -> None:
        self.id = data['id']
        self.title = data['title']
        self.description = data['description']
        self.price = data['price']
        self.user_id = data['user_id'] #! This is a many to many relationship. So you want to access the user id in order to put the many paintings.
        self.first_name = data['first_name'] # Adding this allows you to show the who the painting was posted by. Also referenec the query in get all.
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']


    #! Create
    @classmethod
    def save(cls, data):
        query = "INSERT INTO paintings (title, description, price, user_id) VALUES (%(title)s, %(description)s, %(price)s, %(user_id)s)"
        result = connectToMySQL(DATABASE).query_db(query, data)
        return result


    #! This method shows all the user paintings on the paintings page.. 
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM paintings JOIN users ON users.id = paintings.user_id;"
        # make sure to call the connectToMySQL function with the schema you are targeting. WHICH MAKES A LIST OF DICTONIERS
        results = connectToMySQL(DATABASE).query_db(query)
        # Create an empty list to append our instances (NEW paintingS) of paintings
        paintings = []
        # Iterate over the db results and create instances of paintings with cls.
        for painting in results:
            paintings.append( cls(painting) )
        return paintings
    
    # Read one and adding the one to many relationship 
    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM paintings JOIN users ON users.id = paintings.user_id WHERE paintings.id = %(id)s;" #! STUDYYYY
        result =  connectToMySQL(DATABASE).query_db(query, data) 
        return cls(result[0])
    
    @staticmethod
    def validate_painting(painting):
        print(type(painting['price']))
        is_valid = True 
        if len(painting['description']) < 10:
            flash('Description must be at least 3 chararacters')
            is_valid = False
        if len(painting['title']) < 2:
            flash('Title must be at least 2 chararacters')
            is_valid = False
        if  not painting['price']:
            flash('Please Enter Price')
            is_valid = False
        if  painting['price'] and int((painting['price'])) <= 0:
            print(type(painting['price']))
            flash('Price must be at great than $0')
            is_valid = False
            #! ADDDDDD PRICE
        return is_valid
    
    #!UPDATE
    @classmethod
    def update(cls, data):
        query = "UPDATE paintings SET title=%(title)s, description=%(description)s, price=%(price)s, user_id=%(user_id)s WHERE id= %(id)s"
        return connectToMySQL(DATABASE).query_db(query, data) 

    @classmethod
    def destory(cls, data):
        query = 'DELETE FROM paintings WHERE id = %(id)s'
        return connectToMySQL(DATABASE).query_db(query, data)