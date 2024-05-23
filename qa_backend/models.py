# models.py
from app import db  # Make sure to import db from your Flask app

from flask_login import UserMixin

class User(db.Model, UserMixin):
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(64), unique=True, nullable=False)
    account_number = db.Column(db.String(120), unique=True)
    user_password = db.Column(db.String(255), nullable=False)
    def to_dict(self):
        return {
            "user_id": self.user_id,
            "username": self.user_name
            # include other fields as needed
        }
    def get_id(self):
        return str(self.user_id)  # ensure this returns a string, Flask-Login expects the user ID to be a string

    @property
    def is_active(self):
        # This should return True unless you have a reason to disable accounts
        return True
    @property
    def is_authenticated(self):
        # Add custom logic here if needed, otherwise it defaults to True if the user is logged in
        return True
    @property
    def is_anonymous(self):
        # Typically returns False for authenticated users
        return False

class Document(db.Model):
    __tablename__ = 'documents'
    doc_id = db.Column(db.Integer, primary_key=True)
    doc_name = db.Column(db.String(50), nullable=False)
    txt_content = db.Column(db.Text, nullable=False)
    txt_uploader_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    #txt_uploader_name = db.Column(db.String(64), db.ForeignKey('users.user_name'))  # Assuming user names are stored as strings
    txt_uploader_name = db.Column(db.String(64))  # Assuming user names are stored as strings
    txt_createtime = db.Column(db.DateTime, server_default=db.func.now())
    txt_kind = db.Column(db.Integer, nullable=False)
    def get_access_status(self):
        # if self.is_globally_disabled:
        #     return "disabled"
        
        access_granted = DocumentAccess.query.filter_by(doc_id=self.doc_id, access_right=True).count()
        total_users = User.query.count()

        if access_granted == total_users:
            return "enabled"
        elif access_granted > 0:
            return "partial"
        else:
            return "disabled"

    def __repr__(self):
        return f'<Document {self.doc_name}>'

class DocumentAccess(db.Model):
    __tablename__ = 'document_access'
    access_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    doc_id = db.Column(db.Integer, db.ForeignKey('documents.doc_id'))
    access_right = db.Column(db.Boolean, nullable=False)

    # Define the relationship to Document document as a single instance of Class Docu..
    document = db.relationship('Document', backref='accesses')
    def __repr__(self):
        return f'<DocumentAccess {self.access_id}>'

class Feedback(db.Model):
    __tablename__ = 'feedback'
    feedback_id = db.Column(db.Integer, primary_key=True)
    feedback_name = db.Column(db.String(64), db.ForeignKey('users.user_name'))
    feedback_content = db.Column(db.Text, nullable=False)
    feedback_createtime = db.Column(db.DateTime, server_default=db.func.now())

    def __repr__(self):
        return f'<Feedback {self.feedback_id}>'


class ChatHistory(db.Model):
    __tablename__ = 'chathistory'

    query_id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(20), db.ForeignKey('users.user_name'), nullable=False)
    query_question = db.Column(db.Text, nullable=False)
    accessed_docs = db.Column(db.Text)  # Stores document names accessed during the query
    answer = db.Column(db.Text, nullable=False)
    answer_time = db.Column(db.DateTime, default=db.func.current_timestamp())

    def __repr__(self):
        return f'<ChatHistory {self.query_id}>'
