from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
import bcrypt
from sqlalchemy import CheckConstraint, func

db=SQLAlchemy()

class UserData(db.Model):
    __tablename__='users'
    username = db.Column(db.String(30), unique=True,primary_key=True)
    password = db.Column(db.String(20))

    def __init__(self, username, password):
        self.username = username
        self.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))
 
    

class Section(db.Model):
    __tablename__='sections'
    section_name=db.Column(db.String(50),primary_key=True)
    date_created=db.Column(db.String)
    description=db.Column(db.String)

    def __init__(self,name,description):
        self.section_name=name
        self.description=description
        self.date_created=datetime.today().strftime("%d-%m-%Y")



class Books(db.Model):
    __tablename__='books'
    book_id=db.Column(db.Integer,unique=True,primary_key=True,autoincrement=True)
    name=db.Column(db.String,nullable=False)
    image = db.Column(db.String)
    content = db.Column(db.String)
    author=db.Column(db.String,nullable=False)
    section_name = db.Column(db.Integer, db.ForeignKey('sections.section_name'))
    section = db.relationship('Section', backref='books')

    def __init__(self, name, author,image,content, section):
        self.name = name
        self.author = author
        self.image=image
        self.content=content
        self.section_name = section.section_name
        self.section=section
   


class Requested(db.Model):
    __tablename__='requested'
    request_id=db.Column(db.Integer,autoincrement=True,primary_key=True)
    username=db.Column(db.String,db.ForeignKey('users.username'),nullable=False)
    book_id=db.Column(db.String,db.ForeignKey('books.book_id'),nullable=False)
    requested_at=db.Column(db.DateTime,default=datetime.utcnow)
    days_requested=db.Column(db.Integer)
    status=db.Column(db.String(30),default='Pending')
    issued_at=db.Column(db.DateTime)
    return_date=db.Column(db.DateTime)

    def __init__(self,username,book_id,days):
        self.username=username
        self.book_id=book_id
        self.days_requested=days
        
    def issue_book(self):
        self.status="Issued"
        self.issued_at=datetime.utcnow()
        self.return_date=self.issued_at+timedelta(days=self.days_requested)
    


class Feedback(db.Model):
    __tablename__="feedback"
    feedback_id=db.Column(db.Integer,autoincrement=True,primary_key=True)
    username=db.Column(db.String,db.ForeignKey('users.username'),nullable=False)
    book_id=db.Column(db.String,db.ForeignKey('books.book_id'),nullable=False)
    rating=db.Column(db.Integer, CheckConstraint('rating >= 0 AND rating <= 5'))
    feedback=db.Column(db.String)

    def __init__(self,username,book_id,feedback,rating):
        self.username=username
        self.book_id=book_id
        self.feedback=feedback
        self.rating=rating
    
    @staticmethod
    def calculate_avg_rating(book_id):
        average_rating = db.session.query(
        func.avg(Feedback.rating).label('average_rating')).filter(Feedback.book_id == book_id).scalar()
        if average_rating is not None:
            average_rating = round(average_rating, 2)
        return average_rating