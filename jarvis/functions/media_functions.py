import cv2
from datetime import datetime

video_recording = False
video_writer = None
video_capture = None

def capture_photo():
    """Capture a photo using the webcam."""
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    if ret:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"static/photo_{timestamp}.jpg"
        cv2.imwrite(filename, frame)
        print(f"Photo saved as {filename}")
    cap.release()

def start_video_recording():
    """Start video recording using the webcam."""
    global video_recording, video_writer, video_capture
    video_capture = cv2.VideoCapture(0)
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"static/video_{timestamp}.avi"
    video_writer = cv2.VideoWriter(filename, fourcc, 20.0, (640, 480))

    video_recording = True
    while video_recording and video_capture.isOpened():
        ret, frame = video_capture.read()
        if ret:
            video_writer.write(frame)
    stop_video_recording()

def stop_video_recording():
    """Stop video recording."""
    global video_writer, video_capture, video_recording
    if video_writer:
        video_writer.release()
        video_writer = None
    if video_capture:
        video_capture.release()
        video_capture = None
    video_recording = False
    print("Video recording stopped.")
