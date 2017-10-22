from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:password@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)


Blog = []

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(480))

    def __init__(self, name):
        self.name = name
        self.completed = False

db.create_all()

@app.route('/', methods=['POST', 'GET'])
def index():

    if request.method == 'POST':
        blog_name = request.form['blog']
        new_blog = Blog(blog_name)
        db.session.add(new_blog)
        db.session.commit()

    blogs = Blog.query.all()
    return render_template('add-a-blog.html',title="Build a Blog", blogs=blogs)

@app.route('/blogpost', methods=['GET', 'POST'])
def blogpost():
    id = request.args.get('id')
    if id:
        return 
    
    blog = db.session.query(Blog).filter(Blog.id == id).first()

    
    return render_template('blogpost.html', head="Blog Post {0}".format(id))

@app.route('/newpost', methods=['POST', 'GET'])
def newblog():
    title = ''
    body = ''
    title_error = ''
    body_error = ''
    error = False
    
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
    
    if title.strip() == '':
            title_error = "Try harder"
            error = True

    if body.strip() == '':
            body_error = "Try Harder"
            error = True

    if error is False:
            blog = db.session.add(Blog(title, body))
            db.session.commit()
            
            blog = Blog.query.get(id)
                return redirect('/blogpost?id={0}'.format(blog.id))
    
    return render_template('newpost.html', title=title, head="New Blog",
    body=body, title_error=title_error, body_error=body_error)



if __name__ == '__main__':
    app.run()


















