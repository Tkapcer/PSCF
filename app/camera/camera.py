import cv2

def generate_frames(camera_url, brightness, contrast):
    cap = cv2.VideoCapture(camera_url)

    success, frame = cap.read()
    if not success:
        return None

    while True:
        success, frame = cap.read()
        if not success:
            break
        else:
            frame = cv2.convertScaleAbs(frame, alpha=contrast, beta=brightness)
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    cap.release()