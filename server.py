from flask import Flask, request
import subprocess
import os

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/upload', methods=['POST'])
def upload():

    file = request.files['csvfile']
    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)

    subprocess.run(["gcc","attendance.c","-o","attendance"])

    if os.name=="nt":
        subprocess.run(["attendance.exe",filepath])
    else:
        subprocess.run(["./attendance",filepath])

    subprocess.run(["python","send_email.py"])

    return "<h2>Attendance Checked & Emails Sent Successfully</h2>"

if __name__=="__main__":
    app.run(debug=True)