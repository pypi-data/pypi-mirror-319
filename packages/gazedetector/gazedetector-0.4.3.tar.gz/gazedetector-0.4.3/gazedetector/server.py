from flask import Flask, jsonify, Response, send_from_directory, request, send_file
from flask_cors import CORS
from .detector import GazeDetector
import os

app = Flask(__name__)
CORS(app)

detector = GazeDetector()

@app.route('/video_feed')
def video_feed():
    def gen():
        while True:
            status, frame = detector.detect()
            if frame is not None:
                _, buffer = cv2.imencode('.jpg', frame)
                frame = buffer.tobytes()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
    return Response(gen(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/status')
def status():
    status, _ = detector.detect()
    return jsonify(status=status)

@app.route('/')
def index():
    html_file = request.args.get('html_file', 'index.html')
    return send_file(html_file)

@app.route('/toggle_camera', methods=['POST'])
def toggle_camera():
    global detector
    if detector:
        detector.release()
        detector = None
        return jsonify(status="Camera turned off")
    else:
        detector = GazeDetector()
        return jsonify(status="Camera turned on")

def run_server(toggle_button=True, paste_in_html="index.html", pos={"w": "200px", "h": "100px"}, alignment="mid"):
    global detector

    # Ensure user-provided HTML file exists
    if not os.path.exists(paste_in_html):
        raise FileNotFoundError(f"The specified HTML file '{paste_in_html}' does not exist.")
        
    # Add positional styling for facecam
    facecam_style = f"position: fixed; top: 10px; right: 10px; width: {pos['w']}; height: {pos['h']};"
    if alignment == "mid":
        facecam_style = f"position: fixed; top: 10px; right: 50%; transform: translateX(50%); width: {pos['w']}; height: {pos['h']};"

    # Read the content of the user-provided HTML file
    with open(paste_in_html, 'r') as file:
        content = file.read()

    # Insert positional styling and facecam into the HTML content
    content = content.replace('<img src="http://127.0.0.1:5000/video_feed" id="facecam">', f'<img src="http://127.0.0.1:5000/video_feed" id="facecam" style="{facecam_style}">')

    # Write the modified content to a temporary file to serve
    modified_html_file = 'modified_index.html'
    with open(modified_html_file, 'w') as file:
        file.write(content)

    app.run(debug=True, port=5000)
