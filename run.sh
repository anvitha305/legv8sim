python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt --break-system-packages
python3 -m PyInstaller app.py
