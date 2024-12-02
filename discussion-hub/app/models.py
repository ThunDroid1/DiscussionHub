from flask_sqlalchemy import SQLAlchemy

# Initialize the SQLAlchemy object
db = SQLAlchemy()

class Thread(db.Model):
    __tablename__ = 'thread'  # Specify table name if different from class name
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(50), nullable=False)  # Added author column
    timestamp = db.Column(db.DateTime, index=True, default=db.func.now())
    comments = db.relationship('Comment', backref='thread', lazy=True)

    def __repr__(self):
        return f'<Thread {self.title}>'

class Comment(db.Model):
    __tablename__ = 'comment'  # Specify table name if different from class name
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(50), nullable=False)  # Added author column
    upvotes = db.Column(db.Integer, default=0)
    timestamp = db.Column(db.DateTime, index=True, default=db.func.now())
    thread_id = db.Column(db.Integer, db.ForeignKey('thread.id'), nullable=False)
    parent_id = db.Column(db.Integer, db.ForeignKey('comment.id'))
    parent = db.relationship('Comment', remote_side=[id], backref='replies')

    def __repr__(self):
        return f'<Comment {self.content[:20]}>...'  # Show first 20 characters of the comment
