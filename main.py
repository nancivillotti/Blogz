from flask import Flask, request, redirect, render_template, session, flash, url_for
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:build-a-blog@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    blog_title = db.Column(db.String(120))
    blog_entry = db.Column(db.String(3000))
    

    def __init__(self, blog_title, blog_entry):
        self.blog_entry = blog_entry
        self.blog_title = blog_title
        
    def validation(self):
        if self.blog_entry and self.blog_title:
            return True
        else:
            return False
   
@app.route('/blog', methods=['POST', 'GET']) #displays ALL blog posts
def display_entries():

    post_id = request.args.get('id')
    if (post_id):
        entry = Blog.query.get(post_id)
        return render_template('singlepost.html', title="Single Blog Entry", entry=entry)
    
    else:
        all_entries = Blog.query.all()
        return render_template('blog.html', title="All Blog Posts!", all_entries=all_entries)

@app.route('/newpost', methods=['POST', 'GET']) #enter new entries here
def newpost():
    if request.method == 'POST':
        blog_title = request.form['blog_title']
        post_name = request.form['post']
        new_entry = Blog(blog_title, post_name)

        if new_entry.validation():

            db.session.add(new_entry)
            db.session.commit()
            single_entry = "/blog?id=" + str(new_entry.id)
            return redirect(single_entry)

        
        else:
            flash ("Fill out all the fields you slacker!!", "error")
            return render_template('newpost.html')
    else:
        return render_template ('newpost.html')

    

if __name__ == '__main__':
    app.run()