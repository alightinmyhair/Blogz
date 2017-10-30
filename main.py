#goal is to make a multi-user blog site
#to do:
#------add templates: signup.html, login.html, index.html, singleuser.html
#------add route handlers: signup, login, index
#------create a logout function that handles POST request to /logout and redirects to /blog after deleting username
#------add a user class
from flask import Flask, request, redirect, render_template, flash, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:beproductive@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'y337kGcys&zP3B'


class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(60))
    body = db.Column(db.String(120))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id')) #come back to this

    def __init__(self, title, body, owner):
        self.title = title
        self.body = body
        self.owner = owner

class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50))
    password = db.Column(db.String(20))
    blogs = db.relationship('Blog', backref = 'owner')  #look at closely

    def __init__(self, username, password):
        self.username = username
        self.password = password

@app.before_request
def require_login():
    allowed_routes = ['login_page', 'blogz', 'home_page', 'show_blog', 'blog_post', 'validate_signin']
    if request.endpoint not in allowed_routes and 'username' not in session:
        return redirect('/login')

@app.route('/home', methods = ['GET'])
def home_page():
    request.method == 'GET'
    #user_info = request.args['username']
    #username = request.form['username']
    #user_id = int(request.args['id'])
    #user = Blog.query.get(username)
    users = User.query.all()
    return render_template('index.html', title = "Blogz", users=users)

@app.route('/blog', methods=['POST', 'GET'])
def blogz():  
    #request.method=='GET'
    #users = username
    blogs = Blog.query.all()
    users = User.query.all()
    return render_template('blog.html',title="Blogz!", blogs=blogs, users=users)


@app.route('/newpost', methods=['POST'])
def new_blog():

    # blogs = Blog.query.all()

    #if request.method == 'POST':
    blogbody = request.form['blogbody']
    titleblog = request.form['titleblog']
    username = session.get('username') 
    # user_id = session.get('id')
    user_id = User.query.filter_by(username=username).first()
    users = User.query.all()

    titleblog_error = ''
    blogbody_error = ''

    if blog_entry(titleblog):
        titleblog_error = "Make sure you enter a title"

    if blog_entry(blogbody):
        blogbody_error = "Make sure you add content"

    if titleblog_error or blogbody_error:
        return render_template('newpost.html', titleblog_error=titleblog_error, blogbody_error=blogbody_error, blogbody=blogbody, titleblog=titleblog)

    new_blog = Blog(titleblog, blogbody, user_id)         

    db.session.add(new_blog)
    db.session.commit()

    blogs = Blog.query.all()

    blog_id = Blog.query.filter(Blog.title == titleblog).first()
    blog_id = blog_id.id
    
    return render_template('singlepost.html', blogs=blogs, users=users, blog_id=blog_id)


    
@app.route('/newpost', methods=['GET'])
def get_info():
    blogs = Blog.query.all()
    return render_template('newpost.html', title="Blogz!", blogs=blogs)



@app.route('/post', methods=['POST', 'GET'])
def show_blog():
    request.method == 'GET'
    user_id = int(request.args['user_id'])

    blogs = Blog.query.all()
    users = User.query.all()

    if user_id == None:
        user_id = 0


    return render_template('post.html',title="Blogz!", users=users, blogs=blogs, user_id=user_id) #blog_id=blog_id)

@app.route('/singlepost', methods=['GET'])

def blog_post():
    request.method == 'GET'
    blog_id = int(request.args['blog_id'])

    blogs = Blog.query.all()
    users = User.query.all()
    
    return render_template('singlepost.html', title="Blogz!", users=users, blogs=blogs, blog_id=blog_id)

@app.route('/login', methods=['POST', 'GET'])
#correct username/password route to /newpost
#incorrect username and/or correct username but wrong password, redirect to /login
#username and password is incorrect,direct to signup


def login_page():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            session['username'] = username
            session['id'] = user.id
            return redirect('/newpost')
        if user and user.password != password:
            session['username'] = username
            flash('Password is incorrect', 'error')
            return redirect('/login')

        #incorrect username and/or correct username but wrong password, redirect to /login
        if user != username:
            session['username'] = username
            flash('Username is incorrect', 'error')
            return redirect('/login')
        # else:-
        #     flash('Password is incorrect, or username does not exist. You should create an account', 'error')
        #     return redirect('/login')
    # else:

    if request.method == 'GET':
        return render_template('login.html')

def blog_entry(word):
    new_word = word.strip()
    if len(new_word) ==0:
        return True
    else:
        return False

def char_length(word):
    if " " in word:
        return True
    if 3< len(word) <20:
        return False
    else:
        return True

def is_blank(word):
    if word.strip != 0:
        return False
    else:
        return True

def samepassword_check(word, verify_word):
    if word == verify_word:
        return False
    else:
        return True

@app.route("/signup", methods=['POST', 'GET'])  #work on check for username
def validate_signin():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        verify_password = request.form['verify_password']
        user = User.query.filter_by(username=username).first()
    
        username_error = ''
        sameusername_error = ''
        password_error = ''
        verify_password_error = ''
        
        if is_blank(username):
            username_error = 'Username field must not be empty'

        if char_length(username):
            username_error = 'Username must not contain a space and be between 3-20 characters long' 

        if char_length(password):
            password_error = 'Password must not contain a space and be between 3-20 characters long'
        
        if user and user.username == username:
            sameusername_error = 'Username already taken'

        if samepassword_check(password, verify_password):
            verify_password_error = 'Passwords must match'
        
        if username_error or password_error or sameusername_error or verify_password_error:
            return render_template('signup.html', username=username, password_error=password_error, username_error=username_error, verify_password_error=verify_password_error, sameusername_error=sameusername_error)
        
        else:
            new_user = User(username,password)
            db.session.add(new_user)
            db.session.commit()
            session['username'] = username
            return redirect('/newpost')
    else:
        return render_template('signup.html')


@app.route('/logout')
def logout():
    del session['username']
    return redirect('/blog')

if __name__ == '__main__':
    app.run()