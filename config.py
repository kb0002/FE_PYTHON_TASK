import os

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "supersecretkey")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "mysql+mysqlconnector://user:password@localhost/video_db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = "uploads"
    KAFKA_BROKER = "localhost:9092"
    KAFKA_TOPIC = "video-stream"
