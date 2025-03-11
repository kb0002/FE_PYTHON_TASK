from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    encryption_key = db.Column(db.String(255), nullable=False)  # Store the key securely
    uploaded_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    def to_dict(self):
        return {
            "id": self.id,
            "filename": self.filename,
            "uploaded_at": self.uploaded_at
        }
