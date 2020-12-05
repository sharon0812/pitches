from . import db
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin,current_user
from . import login_manager
from datetime import datetime




@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class PhotoProfile(db.Model):
    __tablename__ = 'profile_photos'

    id = db.Column(db.Integer,primary_key = True)
    pic_path = db.Column(db.String())
    user_id = db.Column(db.Integer,db.ForeignKey("users.id"))

class User(UserMixin,db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(255))
    email = db.Column(db.String(255),unique = True,index = True)
    role_id = db.Column(db.Integer,db.ForeignKey('roles.id'))
    bio = db.Column(db.String(255))
    profile_pic_path = db.Column(db.String())
    password_hash = db.Column(db.String(255))
    photos = db.relationship('PhotoProfile',backref = 'user',lazy = "dynamic")
    pitch = db.relationship('Pitch',backref = 'user',lazy = "dynamic")
    downvotes = db.relationship('Downvote',backref = 'user',lazy = "dynamic")
    upvotes = db.relationship('Upvote',backref = 'user',lazy = "dynamic")
    

    @property
    def password(self):
        raise AttributeError('You cannnot read the password attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)


    def verify_password(self,password):
        return check_password_hash(self.password_hash,password)

    def __repr__(self):
        return f'User {self.username}'
    
class Pitch(db.Model):
    '''
    Pitch class to define Pitch Objects
    '''
    __tablename__ = 'pitch'

    id = db.Column(db.Integer,primary_key = True)
    pitch = db.Column(db.String)
    category_id = db.Column(db.Integer)
    date = db.Column(db.DateTime,default=datetime.utcnow)
    user_id = db.Column(db.Integer,db.ForeignKey("users.id"))
    comments = db.relationship('Comment',backref = 'pitch',lazy="dynamic")
    upvotes = db.relationship('Upvote', backref = 'pitch', lazy = 'dynamic')
    downvotes = db.relationship('Downvote', backref = 'pitch', lazy = 'dynamic')
        

    def save_pitch(self):
        '''
        Function that saves pitches
        '''
        db.session.add(self)
        db.session.commit()
    
    @classmethod
    def get_all_pitches(cls):
        '''
        Function that queries the databse and returns all the pitches
        '''
        return Pitch.query.all()

    @classmethod
    def get_pitches_by_category(cls,category_id):
        '''
        Function that queries the databse and returns pitches based on the
        category passed to it
        '''
        return Pitch.query.filter_by(category_id= category_id)


class Role(db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(255))
    users = db.relationship('User',backref = 'role',lazy="dynamic")


    def __repr__(self):
        return f'User {self.name}'


class Comment(db.Model):

    __tablename__ = 'comments'

    id = db.Column(db.Integer,primary_key = True)
    comment = db.Column(db.String)
    image_path = db.Column(db.String)
    pitch_id = db.Column(db.Integer,db.ForeignKey('pitch.id'))
    posted = db.Column(db.DateTime,default=datetime.utcnow)
    username = db.Column(db.String)


    def save_comments(self):
        db.session.add(self)
        db.session.commit()
        

    @classmethod
    def get_comments(cls,id):
        comments = Comment.query.filter_by(pitch_id=id).all()
        return comments


    @classmethod
    def clear_(cls):
        Comment.all_comments.clear()

   

class PitchCategory(db.Model):
    '''
    Function that defines different categories of pitches
    '''
    __tablename__ ='pitch_categories'


    id = db.Column(db.Integer, primary_key=True)
    name_of_category = db.Column(db.String(255))
    category_description = db.Column(db.String(255))

    @classmethod
    def get_categories(cls):
        '''
        This function fetches all the categories from the database
        '''
        categories = PitchCategory.query.all()
        return categories

class Downvote(db.Model):
    __tablename__ = 'downvotes'
    '''
    Function that stores user votes
    '''
    id = db.Column(db.Integer, primary_key=True)
    downvote = db.Column(db.Integer,default=1)
    pitch_id = db.Column(db.Integer,db.ForeignKey('pitch.id'))
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'))

    def save_votes(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def add_downvotes(cls,id):
        downvote_pitch = Downvote(user = current_user, pitch_id=id)
        downvote_pitch.save_downvotes()

    @classmethod
    def get_votes(cls, id):
        downvote = Downvote.query.filter_by(pitch_id=id).all()
        return downvote

    def __repr__(self):
        return f'{self.id_user}:{self.pitch_id}'

class Upvote(db.Model):
    __tablename__ = 'upvotes'
    '''
    Function that stores user votes
    '''
    id = db.Column(db.Integer, primary_key=True)
    upvote = db.Column(db.Integer,default=1)
    pitch_id = db.Column(db.Integer,db.ForeignKey('pitch.id'))
    user_id =  db.Column(db.Integer,db.ForeignKey('users.id'))

    def save_votes(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def add_upvotes(cls,id):
        upvote_pitch = Upvote(user = current_user, pitch_id=id)
        upvote_pitch.save_upvotes()


    @classmethod
    def get_votes(cls, id):
        upvote = Upvote.query.filter_by(pitch_id=id).all()
        return upvote

    def __repr__(self):
        return f'{self.id_user}:{self.pitch_id}' 