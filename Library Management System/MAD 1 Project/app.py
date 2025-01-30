#IMPORTS

import base64
from flask import *
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from flask_sqlalchemy import SQLAlchemy
from matplotlib.backends.backend_agg import FigureCanvasAgg
from datetime import datetime
import  os
import io
from werkzeug.utils import secure_filename
from model import *
matplotlib.use('Agg')
user_book_dict={}

# Create upload folders if they don't exist and specify file types
UPLOAD_FOLDER_IMAGES = 'static/Uploads/images'
UPLOAD_FOLDER_PDFS = 'static/Uploads/pdfs'
ALLOWED_IMAGE_EXTENSIONS = {'png', 'jpg', 'jpeg','webp'}
ALLOWED_CONTENT_EXTENSIONS = {'pdf'}
if not os.path.exists(UPLOAD_FOLDER_IMAGES):
    os.makedirs(UPLOAD_FOLDER_IMAGES)
if not os.path.exists(UPLOAD_FOLDER_PDFS):
    os.makedirs(UPLOAD_FOLDER_PDFS)

#flask app
app = Flask(__name__)
app.config["UPLOAD_IMAGE_FOLDER"]=UPLOAD_FOLDER_IMAGES
app.config["UPLOAD_PDFS_FOLDER"]=UPLOAD_FOLDER_PDFS
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.secret_key = 'pt_iitm_this_is_not_the secret_key'
db.init_app(app)

with app.app_context():
    db.create_all()


#defining all routes
@app.route('/')
def index():
    return render_template('user_login.html')

@app.route("/user_register", methods=['GET', 'POST'])
def user_register():
    if request.method=="POST":
        username=request.form['username']
        password=request.form['password']
        
        if UserData.query.filter_by(username=username).first():
            error_message = "***   Username already exists. Please choose a different username.   ***"
            return render_template('new_user_register.html',error_message=error_message)

        new_user=UserData(username=username,password=password)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('user_login'))
    return render_template("new_user_register.html")



@app.route("/user_login", methods=['GET', 'POST'])
def user_login():
    if request.method=="POST":
        username=request.form['username']
        password=request.form['password']

        user=UserData.query.filter_by(username=username).first() 
        if user and user.check_password(password=password):
            return redirect(url_for('user_dashboard',user_name=username))
        
        error_message="***   Invalid Username and Password.   ***"
        return render_template("user_login.html",error_message=error_message)

    return render_template("user_login.html")



@app.route("/librarian_login", methods=['GET', 'POST'])
def librarian_login():

    if request.method=="POST":
        librarian_name_get=request.form['username']
        librarian_password_get=request.form['password']

        if  librarian_name_get=="Librarian" and librarian_password_get=="librarianpassword":
            return redirect(url_for('librarian_dashboard',librarian_name="Librarian"))
        
        return render_template("librarian_login.html",error_message="*** Invalid Librarian Details. ***")
        
    return render_template('librarian_login.html')



@app.route("/logout")
def logout():
    ref=request.referrer
    if "librarian_dashboard" in ref:
        return redirect(url_for("librarian_login"))
    elif "user_dashboard" in ref:
        return redirect(url_for("user_login"))



@app.route("/user_dashboard/<user_name>") 
def user_dashboard(user_name):
    current_time = datetime.utcnow()
    time_limit_exceed = Requested.query.filter(Requested.return_date <= current_time).all()
    for request in time_limit_exceed:
        db.session.delete(request)

    db.session.commit()
    requested_book_ids = [req.book_id for req in Requested.query.filter(Requested.status=="Pending",Requested.username==user_name)]
    issued_book_ids = [req.book_id for req in Requested.query.filter(Requested.status=="Issued",Requested.username==user_name)]
    books_in_request = Books.query.filter(Books.book_id.in_(requested_book_ids)).all()
    books_issued = Books.query.filter(Books.book_id.in_(issued_book_ids)).all()
    return render_template("user_dashboard_myBooks.html",user_name=user_name,books_in_request=books_in_request,books_issued=books_issued ,section=Section,feedback=Feedback)



@app.route("/user_dashboard/<user_name>/book_store")
def book_store(user_name):
    search_query = request.args.get('search')
    requested_book_ids = [req.book_id for req in Requested.query.filter(Requested.username == user_name)]
    
    if search_query is None:
        books_issued = Books.query.filter(Books.book_id.notin_(requested_book_ids)).all()
    else:
        books_issued = Books.query.filter(Books.book_id.notin_(requested_book_ids),(Books.name.ilike(f'%{search_query}%')) | (Books.author.ilike(f'%{search_query}%'))).all()
    return render_template("book_store.html", user_name=user_name, books_not_in_request=books_issued, feedback=Feedback)



@app.route("/user_dashboard/<user_name>/<book_id>/view_book")
def book_view_user(user_name,book_id):
    return render_template("view_book_user.html",user_name=user_name,book=Books.query.get(book_id),book_id=book_id,feedbacks=Feedback)



@app.route('/user_dashboard/<user_name>/book_store/request/<book_id>',methods=['GET','POST'])
def book_request(user_name, book_id):
    if request.method=="POST":
        nod=request.form['number_of_days']
        requested=Requested(username=user_name,book_id=book_id,days=nod)
        db.session.add(requested)
        db.session.commit()
        return redirect(url_for('book_store',user_name=user_name))
    return render_template("book_store.html",user_name=user_name,books=Books.query.all(),sections=Section.query.all(),req=Requested.query.all())



@app.route("/librarian_dashboard/librarian" ,methods=["GET","POST"])
def librarian_dashboard():
    if request.method == 'POST':
        new_section = Section(name=request.form.get("name"), description=request.form.get("description"))
        db.session.add(new_section)
        db.session.commit()
        return redirect(url_for('librarian_dashboard'))

    return render_template("librarian_dashboard.html",date=datetime.today().strftime("%d-%m-%Y"),sections=Section.query.all())
 


@app.route("/librarian_dashboard/<section_name>", methods=['GET', 'POST'])
def librarian_dashboard_sections(section_name):
    section = Section.query.filter_by(section_name=section_name).first()
    if request.method == 'POST':
        image = request.files['image'] 
        content = request.files['content']
        image_file_type=image.filename.split('.')[-1].lower()
        content_file_type=content.filename.split('.')[-1].lower()

        if image_file_type in ALLOWED_IMAGE_EXTENSIONS:
            filename_image=secure_filename(image.filename)
            image_file_path=os.path.join(app.config["UPLOAD_IMAGE_FOLDER"],filename_image)
            image.save(image_file_path)
        else:
            image_file_path=None
        
        if content_file_type in ALLOWED_CONTENT_EXTENSIONS:
            filename_content=secure_filename(content.filename)
            content_file_path=os.path.join(app.config["UPLOAD_PDFS_FOLDER"],filename_content)
            content.save(content_file_path)
        else:
            content_file_path=None
        
        new_book = Books(name=request.form["name"], author=request.form["author"], image=image_file_path,content=content_file_path, section=section)
        db.session.add(new_book)
        db.session.commit()
        return redirect(url_for('librarian_dashboard_sections', section_name=section.section_name))
    books = section.books
    return render_template("section.html", books=books, section_name=section_name, section=section,feedbacks=Feedback)



@app.route("/librarian_dashboard/<section_name>/edit", methods=["GET", "POST"])
def edit_sections(section_name):
    section = Section.query.get(section_name)
    if request.method == "POST":
        section.section_name = request.form["name"]
        section.description = request.form["description"]
        db.session.add(section)
        db.session.commit()
        return redirect(url_for("edit_sections", section_name=section_name))
    return render_template("librarian_dashboard.html",date=datetime.today().strftime("%d-%m-%Y"),sections=Section.query.all())



@app.route("/librarian_dashboard/<section_name>/delete",methods=["GET","POST"])
def delete_section(section_name):
    section=Section.query.get(section_name)
    for book in Books.query.filter_by(section_name=section_name):
        db.session.delete(book)
    db.session.delete(section)
    db.session.commit()
    
    return render_template("librarian_dashboard.html",date=datetime.today().strftime("%d-%m-%Y"),sections=Section.query.all())



@app.route("/librarian_dashboard/<section_name>/<int:book_id>/view" ,methods=["GET","POST"])
def view_content_lib(section_name,book_id):
    book=Books.query.get(book_id)
    return render_template('view_content_lib.html', section_name=section_name, path=book.content)



@app.route("/user_dashboard/<user_name>/<int:book_id>/view" ,methods=["GET","POST"])
def view_content_user(user_name,book_id):
    book=Books.query.get(book_id)
    return render_template('view_content_user.html', user_name=user_name, path=book.content)



@app.route("/librarian_dashboard/<section_name>/<int:book_id>" ,methods=["GET","POST"])
def book_edit(section_name, book_id):
    book = Books.query.get(book_id)
    if book is None:
        flash('Book not found')
        return redirect(url_for('librarian_dashboard_sections', section_name=section_name))

    if request.method=="POST":
        name_changed = request.form.get('name') != book.name
        author_changed = request.form.get('author') != book.author

        if name_changed:
            book.name = request.form['name']
        if author_changed:
            book.author = request.form['author']
        if 'image' in request.files:
            image_file = request.files['image']
            image_file_type=image_file.filename.split('.')[-1].lower()
            if image_file and image_file_type in ALLOWED_IMAGE_EXTENSIONS:
                    filename_image=secure_filename(image_file.filename)
                    image_file_path=os.path.join(app.config["UPLOAD_IMAGE_FOLDER"],filename_image)
                    image_file.save(image_file_path)
                    book.image = image_file_path
        if 'content' in request.files:
            content_file = request.files['content']
            content_file_type=content_file.filename.split('.')[-1].lower()
            if content_file and content_file_type in ALLOWED_CONTENT_EXTENSIONS:   
                filename_content=secure_filename(content_file.filename)
                content_file_path=os.path.join(app.config["UPLOAD_PDFS_FOLDER"],filename_content)
                content_file.save(content_file_path)
                book.content = content_file_path
        db.session.commit()
        return redirect(url_for('book_edit', section_name=section_name, book_id=book_id))

    return render_template("view_and_edit_book.html", section_name=section_name, book=book, book_id=book_id,feedbacks=Feedback)



@app.route("/librarian_dashboard/<section_name>/<book_id>/delete" ,methods=["GET","POST"])
def book_delete(section_name, book_id):
    book = Books.query.get(book_id)
    if book:
        db.session.delete(book)
        db.session.commit()
    return redirect(url_for('librarian_dashboard_sections', section_name=section_name))



@app.route('/librarian_dashboard/requests')
def request_page():
    return render_template('requests.html',Requested=Requested,Books=Books,UserData=UserData)



@app.route("/librarian_dashboard/approve/<request_id>",methods=["GET","POST"])
def approve_request(request_id):
    if request.method=="POST":
        requested=Requested.query.get(request_id)
        requested.status="issued"
        requested.issue_book()
        db.session.commit()
        return redirect(url_for('approve_request',request_id=request_id))
    return render_template('requests.html',Requested=Requested,Books=Books,UserData=UserData)



@app.route("/librarian_dashboard/deny/<request_id>", methods=["GET", "POST"])
def deny_request(request_id):
    if request.method == "POST":
        requested = Requested.query.get(request_id)
        if requested and requested.username in user_book_dict:  
            user_book_dict[requested.username]=user_book_dict[requested.username]- 1
        db.session.delete(requested)
        db.session.commit()
        return redirect(url_for('deny_request', request_id=request_id))
    return render_template('requests.html', Requested=Requested, Books=Books, UserData=UserData)



@app.route("/user_dashboard/submit_review/<user_name>/<book_id>",methods=["GET","POST"])
def submit_review(user_name,book_id):
    if request.method=="POST":
        feedback=Feedback(username=user_name,book_id=book_id,feedback=request.form['feedback'],rating=request.form["rating"])
        db.session.add(feedback)
        db.session.commit()

    requested_book_ids = [req.book_id for req in Requested.query.filter(Requested.status=="Pending",Requested.username==user_name)]
    issued_book_ids = [req.book_id for req in Requested.query.filter(Requested.status=="Issued",Requested.username==user_name)]
    books_in_request = Books.query.filter(Books.book_id.in_(requested_book_ids)).all()
    books_issued = Books.query.filter(Books.book_id.in_(issued_book_ids)).all()
    return render_template("user_dashboard_myBooks.html",user_name=user_name,books_in_request=books_in_request,books_issued=books_issued ,section=Section,feedback=Feedback)



@app.route("/librarian_dashboard/stats")
def stats_librarian():
    for request in Requested.query.all():
        user_book_dict[request.username]=0
    
    for request in Requested.query.all():
        user_book_dict[request.username]=user_book_dict.get(request.username, 0) + 1
    users=list(user_book_dict.keys())
    books_borrowed=list(user_book_dict.values())
    plt.bar(users, books_borrowed, color='skyblue')
    plt.title('Distribution of Books Among Users')
    plt.xlabel('Users')
    plt.ylabel('Number of Books Borrowed')
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plot_data = buf.read()
    buf.close()
    plot_url = base64.b64encode(plot_data).decode('utf-8')
    return make_response(render_template('stats_librarian.html', plot_url=plot_url))



#run flask app
if __name__ == "__main__":
    app.run(debug=True) 
