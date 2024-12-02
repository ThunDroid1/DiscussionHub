import os
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

# Initialize the Flask application
app = Flask(__name__)

# Configure the app using environment variables
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'default-secret-key')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///database.db')  # Default to SQLite if not set
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database and migration
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Define models
class Thread(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(50), nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=db.func.now())
    comments = db.relationship('Comment', backref='thread', lazy=True)

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(50), nullable=False)
    upvotes = db.Column(db.Integer, default=0)
    timestamp = db.Column(db.DateTime, index=True, default=db.func.now())
    thread_id = db.Column(db.Integer, db.ForeignKey('thread.id'), nullable=False)
    parent_id = db.Column(db.Integer, db.ForeignKey('comment.id'))
    parent = db.relationship('Comment', remote_side=[id], backref='replies')

# Home page with all threads
@app.route('/')
def index():
    threads = Thread.query.order_by(Thread.timestamp.desc()).all()
    return render_template('index.html', threads=threads)

# Individual thread page with comments
@app.route('/thread/<int:thread_id>')
def thread_view(thread_id):
    thread = Thread.query.get_or_404(thread_id)
    comments = Comment.query.filter_by(thread_id=thread_id, parent_id=None).order_by(Comment.upvotes.desc()).all()
    return render_template('thread.html', thread=thread, comments=comments)

# Add a new comment to a thread
@app.route('/thread/<int:thread_id>/comment', methods=['POST'])
def add_comment(thread_id):
    content = request.form['content']
    author = request.form['author']
    if content and author:
        new_comment = Comment(content=content, author=author, thread_id=thread_id)
        db.session.add(new_comment)
        db.session.commit()
    return redirect(url_for('thread_view', thread_id=thread_id))

# Upvote a comment
@app.route('/comment/<int:comment_id>/upvote', methods=['POST'])
def upvote(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    comment.upvotes += 1
    db.session.commit()
    return redirect(url_for('thread_view', thread_id=comment.thread_id))

# Add a reply to a comment
@app.route('/comment/<int:comment_id>/reply', methods=['POST'])
def reply_to_comment(comment_id):
    parent_comment = Comment.query.get_or_404(comment_id)
    content = request.form['content']
    author = request.form['author']
    if content and author:
        new_reply = Comment(content=content, author=author, thread_id=parent_comment.thread_id, parent_id=parent_comment.id)
        db.session.add(new_reply)
        db.session.commit()
    return redirect(url_for('thread_view', thread_id=parent_comment.thread_id))

# Add a new thread
@app.route('/add_thread', methods=['POST'])
def add_thread():
    title = request.form['title']
    content = request.form['content']
    author = request.form['author']
    if title and content and author:
        new_thread = Thread(title=title, content=content, author=author)
        db.session.add(new_thread)
        db.session.commit()
    return redirect(url_for('index'))

# Create database tables if not already created
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    with app.app_context():
        app.run(debug=True)
