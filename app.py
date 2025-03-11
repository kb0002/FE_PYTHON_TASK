import os
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from kafka import KafkaProducer
from config import Config
from models import db, Video
from encryption import generate_key, encrypt_video, decrypt_video

app = Flask(__name__)
app.config.from_object(Config)
CORS(app)

db.init_app(app)

# Kafka Producer
producer = KafkaProducer(bootstrap_servers=Config.KAFKA_BROKER)

# Ensure upload folder exists
os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)

@app.route("/upload", methods=["POST"])
def upload_video():
    if "video" not in request.files:
        return jsonify({"error": "No video file provided"}), 400
    
    video = request.files["video"]
    if video.filename == "":
        return jsonify({"error": "Invalid file name"}), 400
    
    filename = secure_filename(video.filename)
    file_path = os.path.join(Config.UPLOAD_FOLDER, filename)
    video.save(file_path)

    # Encrypt video
    encryption_key = generate_key()
    encrypted_path = encrypt_video(file_path, encryption_key)

    # Save metadata in DB
    new_video = Video(filename=filename + ".enc", encryption_key=encryption_key.decode())
    db.session.add(new_video)
    db.session.commit()

    return jsonify({"message": "Video uploaded successfully", "video_id": new_video.id}), 201

@app.route("/video/<int:video_id>", methods=["GET"])
def get_video(video_id):
    video = Video.query.get(video_id)
    if not video:
        return jsonify({"error": "Video not found"}), 404

    file_path = os.path.join(Config.UPLOAD_FOLDER, video.filename)

    if not os.path.exists(file_path):
        return jsonify({"error": "File not found"}), 404

    return send_file(file_path, as_attachment=True)

@app.route("/stream/<int:video_id>", methods=["GET"])
def stream_video(video_id):
    video = Video.query.get(video_id)
    if not video:
        return jsonify({"error": "Video not found"}), 404

    file_path = os.path.join(Config.UPLOAD_FOLDER, video.filename)

    if not os.path.exists(file_path):
        return jsonify({"error": "File not found"}), 404

    # Decrypt video
    decrypted_data = decrypt_video(file_path, video.encryption_key.encode())

    # Send to Kafka
    producer.send(Config.KAFKA_TOPIC, decrypted_data)

    return jsonify({"message": "Video streaming started"}), 200

if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Create tables if they don't exist
    app.run(debug=True)
