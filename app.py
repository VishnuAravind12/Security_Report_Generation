import os
import subprocess
from flask import Flask, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
from dotenv import load_dotenv
import base64
from openai import OpenAI
import cv2

load_dotenv()

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['FRAMES_FOLDER'] = 'frames'
app.config['REPORT_FOLDER'] = 'reports'
app.config['ALLOWED_EXTENSIONS'] = {'mp4', 'avi', 'mov', 'mkv'}

openai_api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY", ""))

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

if not os.path.exists(app.config['FRAMES_FOLDER']):
    os.makedirs(app.config['FRAMES_FOLDER'])

if not os.path.exists(app.config['REPORT_FOLDER']):
    os.makedirs(app.config['REPORT_FOLDER'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


def extract_frames(video_path, interval):
    cap = cv2.VideoCapture(video_path)
    frame_rate = cap.get(cv2.CAP_PROP_FPS)
    interval_frames = int(frame_rate * interval)
    frame_count = 0
    base64_frames = []

    if not os.path.exists(app.config['FRAMES_FOLDER']):
        os.makedirs(app.config['FRAMES_FOLDER'])

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        if frame_count % interval_frames == 0:
            frame_filename = os.path.join(app.config['FRAMES_FOLDER'], f'frame_{frame_count}.jpg')
            cv2.imwrite(frame_filename, frame)
            _, buffer = cv2.imencode(".jpg", frame)
            base64_frames.append(base64.b64encode(buffer).decode("utf-8"))
        frame_count += 1
    cap.release()
    return base64_frames


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        video_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(video_path)
        interval = int(request.form['interval'])
        
        print(f"Extracting frames from {video_path} at {interval}-second intervals...")
        base64_frames = extract_frames(video_path, interval)
        print(f"Extracted {len(base64_frames)} frames.")
        
        # Define the prompt with a clear example of the desired format
        prompt_messages = [
            {
                "role": "user",
                "content": [
                    "These are frames from a security camera footage of a robbery. You are a security officer tasked with filling out a theft incident report form in the format below. Follow the format provided below exactly. Identify and describe the following for each suspect: race, gender, whether or not the suspect was armed (you must be extremely sensitive to possible arms), the attire each suspect was wearing and the color of the attire, and whether or not the frame is a good still shot photo of the suspect (include the frame number). Also, determine the duration of the incident, the start time of the incident, and the date of the incident.",
                    *map(lambda x: {"image": x, "resize": 768}, base64_frames),
                    """
### Theft Incident Report

**Date of Incident:** [Insert Date]
**Start Time of Incident:** [Insert Start Time]
**End Time of Incident:** [Insert End Time]
**Duration:** Approximately [Insert Duration]

#### Suspect Details:

**Suspect 1:**
- **Race:** [Insert Race]
- **Gender:** [Insert Gender]
- **Armed:** [Insert Weapon Status]
- **Attire:** [Insert Attire]
- **Good Still Shot:** [Insert Yes/No], Frame Number: [Insert Frame Number]
  
**Suspect 2:**
- **Race:** [Insert Race]
- **Gender:** [Insert Gender]
- **Armed:** [Insert Weapon Status]
- **Attire:** [Insert Attire]
- **Good Still Shot:** [Insert Yes/No], Frame Number: [Insert Frame Number]

### General Summary of the Incident:

[Provide a summary of the incident here]
                    """
                ],
            },
        ]
        
        params = {
            "model": "gpt-4o",
            "messages": prompt_messages,
            "max_tokens": 1000,
        }
        
        try:
            result = client.chat.completions.create(**params)
            report_content = result.choices[0].message.content
            report_id = os.path.splitext(filename)[0]
            report_path = os.path.join(app.config['REPORT_FOLDER'], f'{report_id}.txt')
            with open(report_path, 'w') as f:
                f.write(report_content)
            print(f"Generated report saved to {report_path}.")
            return {"report_content": report_content}
        except Exception as e:
            print(f"Error generating report: {e}")
            return "Error generating report", 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
