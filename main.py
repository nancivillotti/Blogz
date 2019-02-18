from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:build-a-blog@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)


class Blog(db.Model):



    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(100))

    body = db.Column(db.String(1000))



    def __init__(self, title,body):

        self.title = title

        self.body = body



@app.route('/', methods=['POST', 'GET'])

def index():

    return redirect('/blog')





@app.route('/blog', methods=['POST','GET'])

def blog():

    

    if request.args:

        id = request.args.get('id')

        blog = Blog.query.get(id)

        return render_template('viewpost.html', titlebase = 'Build a Blog', blog =blog)





        blogs = Blog.query.all()

        return render_template('blog.html',blogs=blogs)



    else:

        blogs = Blog.query.all()

        return render_template('blog.html', titlebase = 'Build a Blog', blogs=blogs)







@app.route('/newpost', methods=['POST', 'GET'])

def new_post():



    if request.method == 'GET':

        return render_template('newpost.html')



    if request.method == 'POST':

        title_entry = request.form['title']

        body_entry = request.form['body']

        

        title_error=''

        body_error=''



        if len(title_entry) == 0:

            title_error = "You Must Enter a Title For Your Post"

        if len(body_entry) == 0:

            body_error = "You Must Enter A Body For Your Entry"



        if title_error or body_error:

            return render_template('newpost.html', titlebase="New Entry", title_error = title_error, body_error = body_error, title=title_entry, body_name=body_entry)



        else:

            if len(title_entry) and len(body_entry) > 0:

                new_entry = Blog(title_entry, body_entry)

                db.session.add(new_entry)

                db.session.commit()

                return redirect("/blog?id=" + str(new_entry.id))



if __name__ == '__main__':

    app.run()