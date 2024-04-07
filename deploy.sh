pip install -r requirements.txt
cd "lesson3 - client"
gunicorn server_chat:app
