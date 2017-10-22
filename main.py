from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy 


app = Flask(__name__)
app.config['DEBUG']=True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:password@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)

class Blogs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(180))
    body = db.Column(db.String(2000))

    def __init__(self, title, body):
        self.title = title
        self.body = body
    
db.create_all()

@app.route('/', methods = ['POST', 'GET'])
def index():
    
    blog = Blogs.query.all()
    return render_template("index.html", blogs=blog)

@app.route('/blogpost', methods = ['GET','POST'])
def blogpost():
    blog_id = request.args.get('id')
    Blogs_id = request.args.get('id')
    blog = Blogs.query.filter(Blogs.id == blog_id).first()
    return render_template('blogpost.html', blog=blog)



@app.route('/newpost', methods = ['GET','POST'])
def enter_blog():

    if request.method == 'POST':
        title_entry = request.form['title']
        blog_entry = request.form['body']
        title_error = ''
        blog_error = ''
        

        if blog_entry == "" and title_entry == "":
            title_error = "Please put something in the title."
            blog_error = "Please put something in the body."
            return render_template('entries.html',title_entry = title_entry, blog_entry=blog_entry, blog_error=blog_error, title_error=title_error)        
        if title_entry == "":
            title_error = "Please put something in the title."
            return render_template('entries.html',title_entry = title_entry, blog_entry=blog_entry, title_error=title_error)
        if blog_entry == "":
            blog_error = "Please put something in the body."
            return render_template('entries.html',title_entry = title_entry, blog_entry=blog_entry, blog_error=blog_error)
        else:
            new_blog = Blogs(title_entry, blog_entry)
            db.session.add(new_blog)
            db.session.commit()
            db.session.refresh(new_blog)
            return redirect('/blogpost?id=' + str(new_blog.id))

    return render_template('entries.html')

if __name__ == "__main__":
    app.run()
