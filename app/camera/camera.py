import cv2
from config import Config

def generate_frames():
    cap = cv2.VideoCapture(Config.RTSP_URL)
    if not cap.isOpened():
        raise RuntimeError("Nie można połączyć się z kamerą")

    while True:
        success, frame = cap.read()
        if not success:
            break
        _, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')