import os
import pickle
import cv2
import face_recognition
import cvzone
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage
import numpy as np
from datetime import datetime

cred = credentials.Certificate("files/serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://minorproject-f2572-default-rtdb.firebaseio.com/',
    'storageBucket': 'minorproject-f2572.appspot.com'
})

bucket = storage.bucket()

cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

imgBackground = cv2.imread('Resources/background.png')

# Importing the mode images into a list
folderModePath = 'Resources/Modes'
modePathList = os.listdir(folderModePath)
imgModeList = []
for path in modePathList:
    imgModeList.append(cv2.imread(os.path.join(folderModePath, path)))
# print(len(imgModeList))

# Load the encoding file
print("Loading Encode File ...")
file = open('EncodeFile.p', 'rb')
encodeListKnownWithIds = pickle.load(file)
file.close()
encodeListKnown, studentIds = encodeListKnownWithIds
# print(studentIds)
print("Encode File Loaded")

modeType = 0
counter = 0
id = -1
imgStudent = []

while True:
    success, img = cap.read()

    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    faceCurFrame = face_recognition.face_locations(imgS)
    encodeCurFrame = face_recognition.face_encodings(imgS, faceCurFrame)

    imgBackground[162:162 + 480, 55:55 + 640] = img
    imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]

    if faceCurFrame:
        for encodeFace, faceLoc in zip(encodeCurFrame, faceCurFrame):
            matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
            faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
            # print("matches", matches)
            # print("faceDis", faceDis)

            matchIndex = np.argmin(faceDis)
            # print("Match Index", matchIndex)

            if matches[matchIndex]:
                # print("Known Face Detected")
                # print(studentIds[matchIndex])
                y1, x2, y2, x1 = faceLoc
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                bbox = 55 + x1, 162 + y1, x2 - x1, y2 - y1
                imgBackground = cvzone.cornerRect(imgBackground, bbox, rt=0)
                id = studentIds[matchIndex]
                if counter == 0:
                    cvzone.putTextRect(imgBackground, "Loading", (275, 400))
                    cv2.imshow("Face Attendance", imgBackground)
                    cv2.waitKey(1)
                    counter = 1
                    modeType = 1

        if counter != 0:

            if counter == 1:
                # Get the Data
                studentInfo = db.reference(f'Students/{id}').get()
                print(studentInfo)
                # Get the Image from the storage
                blob = bucket.get_blob(f'photos/{id}.png')
                array = np.frombuffer(blob.download_as_string(), np.uint8)
                imgStudent = cv2.imdecode(array, cv2.COLOR_BGRA2BGR)
                newImgStudent = cv2.resize(imgStudent, (216, 216))
                # Update data of attendance
                datetimeObject = datetime.strptime(studentInfo['last_attendance_time'],
                                                   "%Y-%m-%d %H:%M:%S")
                secondsElapsed = (datetime.now() - datetimeObject).total_seconds()
                print(secondsElapsed)
                if secondsElapsed > 30:
                    ref = db.reference(f'Students/{id}')
                    studentInfo['total_attendance'] += 1
                    ref.child('total_attendance').set(studentInfo['total_attendance'])
                    ref.child('last_attendance_time').set(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                else:
                    modeType = 3
                    counter = 0
                    imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]

            if modeType != 3:

                if 10 < counter < 20:
                    modeType = 2

                imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]

                if counter <= 10:
                    cv2.putText(imgBackground, str(studentInfo['total_attendance']), (861, 125),
                                cv2.FONT_HERSHEY_COMPLEX, 1, (0,0,0), 1)
                    cv2.putText(imgBackground, str(studentInfo['major']), (1006, 550),
                                cv2.FONT_HERSHEY_COMPLEX, 0.5, (0,0,0), 1)
                    cv2.putText(imgBackground, str(id), (1006, 493),
                                cv2.FONT_HERSHEY_COMPLEX, 0.5, (0,0,0), 1)

                    (w, h), _ = cv2.getTextSize(studentInfo['name'], cv2.FONT_HERSHEY_COMPLEX, 1, 1)
                    offset = (414 - w) // 2
                    cv2.putText(imgBackground, str(studentInfo['name']), (808 + offset, 445),
                                cv2.FONT_HERSHEY_COMPLEX, 1, (50, 50, 50), 1)

                    imgBackground[175:175 + 216, 909:909 + 216] = newImgStudent

                counter += 1

                if counter >= 20:
                    counter = 0
                    modeType = 0
                    studentInfo = []
                    imgStudent = []
                    imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]
    else:
        modeType = 0
        counter = 0
    # cv2.imshow("Webcam", img)
    cv2.imshow("Face Attendance", imgBackground)
    cv2.waitKey(1)


















# import cv2
# import os
# import pickle
# import face_recognition
# import cvzone
# import numpy as np
# import firebase_admin
# from firebase_admin import credentials, db, storage
#
# cred = credentials.Certificate("serviceAccountKey.json")
# firebase_admin.initialize_app(cred, {
#     'databaseURL': 'https://facerecognition-47b6a-default-rtdb.firebaseio.com/',
#     'storageBucket': 'facerecognition-47b6a.appspot.com'
# })
#
# bucket = storage.bucket()
#
# cmp = cv2.VideoCapture(0)
# cmp.set(3, 640)
# cmp.set(4, 480)
#
# imgBackground = cv2.imread('Resources/background.png')
#
# folderModePath = 'Resources/Modes'
# modePathList = os.listdir(folderModePath)
# imgModeList = []
# for path in modePathList:
#     imgModeList.append(cv2.imread(os.path.join(folderModePath, path)))
#
# file = open('encodeFile.p', 'rb')
# encodeListKnownWithIds = pickle.load(file)
# file.close()
#
# encodeListKnown, studentsIds = encodeListKnownWithIds
#
# modeType = 0
# counter = 0
# id = -1
# imgStudent = []
#
# while True:
#     success, img = cmp.read()
#
#     imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
#     imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)
#
#     faceCurFrame = face_recognition.face_locations(imgS)
#     encodeCurFrame = face_recognition.face_encodings(imgS, faceCurFrame)
#
#     imgBackground[162:162 + 480, 55:55 + 640] = img
#     imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]
#
#     for encodeFace, faceLoc in zip(encodeCurFrame, faceCurFrame):
#         matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
#         faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
#
#         matchIndex = np.argmin(faceDis)
#
#         if matches[matchIndex]:
#             y1, x2, y2, x1 = faceLoc
#             y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
#             bbox = 55 + x1, 162 + y1, x2 - x1, y2 - y1
#             imgBackground = cvzone.cornerRect(imgBackground, bbox, rt=0)
#             id = studentsIds[matchIndex]
#             if counter == 0:
#                 counter = 1
#                 modeType = 1
#
#     if counter != 0:
#         if counter == 1:
#             studentsInfo = db.reference(f'students/{id}').get()
#             print(studentsInfo)
#
#             blob = bucket.get_blob(f'photos/{id}.png')
#             array = np.frombuffer(blob.download_as_string(), np.uint8)
#             imgStudent = cv2.imdecode(array, cv2.COLOR_BGRA2BGR)
#
#         cv2.putText(imgBackground, str(studentsInfo['total_attendance']), (861, 125),
#                     cv2.FONT_HERSHEY_COMPLEX, 1, (0,0,0), 2)
#         cv2.putText(imgBackground, str(studentsInfo['major']), (1006, 550),
#                     cv2.FONT_HERSHEY_COMPLEX, 0.5, (0,0,0), 1)
#         cv2.putText(imgBackground, str(id), (1006, 493),
#                     cv2.FONT_HERSHEY_COMPLEX, 0.5, (0,0,0), 1)
#
#         (w, h), _ = cv2.getTextSize(studentsInfo['name'], cv2.FONT_HERSHEY_COMPLEX, 1, 1)
#         offset = (414 - w)//2
#         cv2.putText(imgBackground, str(studentsInfo['name']), (808+offset, 445),
#                     cv2.FONT_HERSHEY_COMPLEX, 1, (50, 50, 50), 1)
#         imgBackground[175:175+216, 909:909+216] = imgStudent
#         counter += 1
#
#     cv2.imshow('Face Attendance', imgBackground)
#     cv2.waitKey(1)