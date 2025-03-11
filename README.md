Steps to Run the Backend (Flask + Kafka + MySQL)

    🔹 Clone the Repository

git clone <your-repo-url> && cd video-streaming-backend

🔹 Create & Activate a Virtual Environment

python -m venv venv && source venv/bin/activate  # macOS/Linux  
venv\Scripts\activate  # Windows

🔹 Install Dependencies

pip install -r requirements.txt

🔹 Setup MySQL Database (Update config.py with DB details)

CREATE DATABASE video_streaming;

🔹 Run Migrations (If Using Flask-Migrate)

flask db upgrade

🔹 Start Apache Kafka (Ensure Zookeeper is running first)

kafka-server-start.sh config/server.properties

🔹 Run Kafka Consumer (for streaming)

python consumer.py

🔹 Start Flask API

python app.py

🔹 Backend Running at: http://localhost:5000
