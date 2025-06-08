import cv2
import os
import urllib.request

haar_urls = {
    "face": "https://raw.githubusercontent.com/opencv/opencv/master/data/haarcascades/haarcascade_frontalface_default.xml",
    "smile": "https://raw.githubusercontent.com/opencv/opencv/master/data/haarcascades/haarcascade_smile.xml"
}

cascade_dir = "cascades"
os.makedirs(cascade_dir, exist_ok=True)

face_path = os.path.join(cascade_dir, "haarcascade_frontalface_default.xml")
smile_path = os.path.join(cascade_dir, "haarcascade_smile.xml")

if not os.path.exists(face_path):
    urllib.request.urlretrieve(haar_urls["face"], face_path)
if not os.path.exists(smile_path):
    urllib.request.urlretrieve(haar_urls["smile"], smile_path)

# Load cascades
face_cascade = cv2.CascadeClassifier(face_path)
smile_cascade = cv2.CascadeClassifier(smile_path)

# Start webcam
cap = cv2.VideoCapture(0)

print("😄 testing 3... Press 'q' to quit.")
while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

    for (x, y, w, h) in faces:
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = frame[y:y+h, x:x+w]

        # Draw face rectangle
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

        # Detect smile inside face ROI
        smiles = smile_cascade.detectMultiScale(
            roi_gray,
            scaleFactor=1.8,
            minNeighbors=20
        )

        for (sx, sy, sw, sh) in smiles:
            cv2.rectangle(roi_color, (sx, sy), (sx+sw, sy+sh), (0, 255, 0), 2)
            cv2.putText(frame, "😊 Smile", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

    cv2.imshow("mr silly 😁", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
