from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy


app=Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI']= 'mysql+pymysql://blogz:blogz@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

app.secret_key="D12345"



class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(800))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, title, body, owner):
        self.title = title
        self.body = body
        self.owner = owner


class User(db.Model):

    id = db.Column(db.Integer, primary_key=True) 
    username = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))
    blogs = db.relationship('Blog', backref='owner')

    def __init__(self, username, password):
        self.username = username
        self.password = password


@app.before_request   
def require_login():
    allowed_routes = ['login','signup', 'blog', 'index']  
    if request.endpoint not in allowed_routes and 'username' not in session:
        return redirect('/login')
 


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form["password"]
        user = User.query.filter_by(username=username).first()  
        if not user:
            flash("Username does not exist")
            return redirect("/login")
        elif user.password != password:
            flash("Incorrect password")
            return redirect("/login")
        else:
            session['username'] = username
            flash("Logged in")
            return redirect("/newpost")
    return render_template("login.html")


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method =='POST':
        username = request.form['username']
        password = request.form['password']
        verify = request.form['verify']

        
        if verify == "" or verify != password:
            flash("The passwords do not match")
            return render_template('signup.html')

        existing_user = User.query.filter_by(username=username).first()  
        if not existing_user:   
            new_user = User(username, password)  
            db.session.add(new_user)
            db.session.commit()
            session['username'] = username 
            return redirect('/')
        else:
            
            return "<h1 class='error'>Duplicate user</h1>"

    return render_template('signup.html')


@app.route('/', methods=['GET', 'POST'])
def index():
    users = User.query.all()
    return render_template('index.html', users=users)


@app.route('/blog', methods=['GET', 'POST'])
def blog():
    
    if request.args:
        blog_id = request.args.get('id')
        user_id = request.args.get('user')
        users = ''
        blogs = ''
                
        if blog_id:
            blogs = Blog.query.get(blog_id)
            return render_template('post.html', blogs=blogs)
        if user_id:
            user = User.query.get(user_id)
            blogs = Blog.query.filter_by(owner=user).all()
            return render_template('singleUser.html', blogs=blogs)
        
    else:
        blogs = Blog.query.all()
       
        return render_template('blog.html', blogs=blogs)


@app.route('/newpost', methods=['GET', 'POST'])
def newpost():       
    
    if request.method == 'POST':
        owner = User.query.filter_by(username=session['username']).first()
        blog_title = request.form['title']
        blog_body = request.form['body']
        title_error = ""
        body_error = ""

        if len(blog_title) == 0:
            title_error = "title must be entered"

        if len(blog_body) == 0:
            body_error = "blog must be entered"

        if not title_error and not body_error:
            updated_blog = Blog(blog_title, blog_body, owner) 
            db.session.add(updated_blog) 
            db.session.commit() 
            query_string = "/blog?id=" + str(updated_blog.id) 
            return redirect(query_string) 
            
        else:
            return render_template('newpost.html', title_error=title_error,body_error=body_error)
    
    else:
         return render_template('newpost.html')




@app.route('/logout')
def logout():
    del session['username']  
    return redirect('/')


if __name__ == '__main__':
    app.run()