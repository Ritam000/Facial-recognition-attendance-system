import os
import django

# Point this script to your Django project's settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'attendance_system.settings')
django.setup()

from admin_panel.models import Student

import face_recognition
import cv2
import numpy as np
import datetime

# Load all students from the database instead of a folder
students = Student.objects.all()

images = []
classNames = []

studentData = []  # will hold (roll_number, enrollment_number, name) for each student

for student in students:
    photo_path = student.photo.path  # full file path on disk
    curImg = cv2.imread(photo_path)
    if curImg is not None:
        images.append(curImg)
        classNames.append(student.name)  # kept for matching index, as before
        studentData.append((student.roll_number, student.name))

def findEncodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encodes = face_recognition.face_encodings(img)
        if len(encodes) > 0:
            encodeList.append(encodes[0])
    return encodeList

def markAttendance(roll_number, name):
    try:
        today_str = datetime.datetime.now().strftime('%A-%Y-%m-%d')
        filepath = os.path.join('attendance', f'{today_str}.csv')
        file_exists = os.path.isfile(filepath)

        with open(filepath, 'a+') as f:
            f.seek(0)
            myDataList = f.readlines()
            rollList = [line.split(',')[0] for line in myDataList]

            if not file_exists or len(myDataList) == 0:
                f.writelines('Roll No,Name,Day & Date,Time\n')

            if str(roll_number) not in rollList:
                now = datetime.datetime.now()
                day_date_str = now.strftime('%A - %Y-%m-%d')
                time_str = now.strftime('%H:%M:%S')
                f.writelines(f'{roll_number},{name},{day_date_str},{time_str}\n')
    except PermissionError:
        print("Could not write to today's attendance file — it might be open in Excel. Please close it and try again.") 


encodeListKnown = findEncodings(images)
print("Encoding Complete")

cap = cv2.VideoCapture(0)

cv2.namedWindow('Webcam', cv2.WINDOW_NORMAL)
cv2.setWindowProperty('Webcam', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

while True:
    success, img = cap.read()
    imgS = cv2.resize(img, (0,0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    facesCurFrame = face_recognition.face_locations(imgS)
    encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)

    for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
        matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
        faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)

        matchIndex = np.argmin(faceDis)

        if matches[matchIndex]:
            roll_number, name = studentData[matchIndex]

            y1, x2, y2, x1 = faceLoc
            y1, x2, y2, x1 = y1*4, x2*4, y2*4, x1*4

            cv2.rectangle(img, (x1,y1), (x2,y2), (0,255,0), 2)
            cv2.putText(img, name, (x1,y2+20),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)

            markAttendance(roll_number,name)

    cv2.imshow('Webcam', img)
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()