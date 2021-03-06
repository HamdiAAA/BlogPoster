from flask import Flask , request, render_template ,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import time

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///posts.db'
db = SQLAlchemy(app)

all_posts = []

class BlogPost(db.Model):
    id = db.Column(db.Integer , primary_key=True)
    title = db.Column(db.String(100) , nullable=False)
    content =db.Column(db.Text , nullable=False)
    author = db.Column(db.String ,nullable=False, default="N/A")
    date_posted = db.Column(db.DateTime ,nullable=False
                            , default=datetime.utcnow )

    def __repr__(self):
        return "Blog post " + str(self.id)

@app.route("/")
def index() :
    return render_template('index.html')

@app.route("/posts", methods=['GET','POST'])
def showPosts():

    if request.method =="POST" :
        post_title = request.form['title']
        post_content = request.form['post']
        post_author = request.form['author']
        post = BlogPost(title=post_title,content=post_content
                        , author=post_author)
        db.session.add(post)
        db.session.commit()
        return redirect('/posts')

    else:
        all_posts = BlogPost.query.order_by(BlogPost.date_posted).all()
        return render_template('posts.html',posts=all_posts)

@app.route('/posts/delete/<int:id>')
def deletePost(id):
    post = BlogPost.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()
    return redirect('/posts')


@app.route('/posts/edit/<int:id>',methods=['GET','POST'])
def editPost(id):
    post = BlogPost.query.get_or_404(id)

    if request.method == "POST":
        post.title = request.form['title']
        post.content = request.form['post']
        post.author = request.form['author']
        db.session.commit()
        return redirect('/posts')
    else:
        return render_template('edit.html',post=post)



@app.route('/home/<string:name>')
def hello(name):
    return f"Hello {name} !"

@app.route('/onlyget' , methods=['get'])


def get_req():
    return "you can only get this webpage !"


if __name__ == "__main__" :
    app.run(debug=True)
