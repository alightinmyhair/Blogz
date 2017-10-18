#to do:
#----1st setup a blog to enter in a post
#----then the /blog route needs to display all of the blog posts
#----able to submit a new post at the /newpost route
#----after submitting a new post my app displays the main blog page
#----make sure i have two templates: one for the main blog listings and a 2nd template from new blogs
#----also make sure I have a base html template
#----if the blog title or the blog body is left empty, the form is rendered again with an error message

#display individual entries:
#-----blogs need to be URL links
#-----create a template page



from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:beproductive@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)


def char_length(word):
    new_word = word.strip()
    if len(new_word) ==0:
        return True
    else:
        return False

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(60))
    body = db.Column(db.String(120))

    def __init__(self, title, body):
        self.title = title
        self.body = body

@app.route('/blog', methods=['POST', 'GET'])
def index():  
    blogs = Blog.query.all()

    return render_template('blog.html',title="Build a Blog!", blogs=blogs)


@app.route('/newpost', methods=['POST'])
def new_blog():

    blogs = Blog.query.all()

    if request.method == 'POST':
        blogbody = request.form['blogbody']
        titleblog = request.form['titleblog']

        titleblog_error = ''
        blogbody_error = ''

        if char_length(titleblog):
            titleblog_error = "Make sure you enter a title"

        if char_length(blogbody):
            blogbody_error = "Make sure you add content"

        if titleblog_error or blogbody_error:
            return render_template('newpost.html', titleblog_error=titleblog_error, blogbody_error=blogbody_error, blogs=blogs, blogbody=blogbody, titleblog=titleblog)

        new_blog = Blog(titleblog, blogbody)          
    
        db.session.add(new_blog)
        db.session.commit()

    return render_template('post.html', blogbody=blogbody, titleblog=titleblog)


    
@app.route('/newpost', methods=['GET'])
def get_info():
    blogs = Blog.query.all()
    return render_template('newpost.html', title="Build a Blog!", blogs=blogs)



@app.route('/post', methods=['POST', 'GET'])
def show_blog():
    request.method == 'GET'
    blog_id = int(request.args['id'])
    blog = Blog.query.get(blog_id)
    titleblog = blog.title
    blogbody = blog.body
    return render_template('post.html',title="Build a Blog!", blogbody=blogbody, titleblog=titleblog)


if __name__ == '__main__':
    app.run()