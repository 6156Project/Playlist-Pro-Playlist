# Playlist-Pro-Playlist
# How to run server
1. Install requirements: `pip install -r requirements.txt`
2. Start server: `python .\src\application.py`

# How to run server on EC2
1. sudo systemctl start gunicorn
2. sudo systemctl enable gunicorn
3. sudo systemctl status gunicorn
