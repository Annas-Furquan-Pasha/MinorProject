import cv2
import face_recognition
import pickle
import os
import firebase_admin
from firebase_admin import credentials, storage

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://facerecognition-47b6a-default-rtdb.firebaseio.com/',
    'storageBucket': 'facerecognition-47b6a.appspot.com'
})

folderPath = 'photos'
imgPathList = os.listdir(folderPath)
imgList = []
studentsIds = []
for path in imgPathList:
    imgList.append(cv2.imread(os.path.join(folderPath, path)))
    studentsIds.append(os.path.splitext(path)[0])

    filename = f'{folderPath}/{path}'
    bucket = storage.bucket()
    blob = bucket.blob(filename)
    blob.upload_from_filename(filename)


def findEncodings(imagesList):
    encodeList = []
    for img in imagesList:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)

    return encodeList

encodeListKnown = findEncodings(imgList)
encodeListKnownWithIds = [encodeListKnown, studentsIds]

file = open('encodeFile.p', 'wb')
pickle.dump(encodeListKnownWithIds, file)
file.close()
# import cv2
# import face_recognition
# import pickle
# import os
# import firebase_admin
# from firebase_admin import credentials
# from firebase_admin import db
# from firebase_admin import  storage
#
# cred = credentials.Certificate("serviceAccountKey.json")
# firebase_admin.initialize_app(cred, {
#     'databaseURL': 'https://facerecognition-47b6a-default-rtdb.firebaseio.com/',
#     'storageBucket': 'facerecognition-47b6a.appspot.com'
# })
#
#
# # Importing student images
# folderPath = 'photos'
# pathList = os.listdir(folderPath)
# print(pathList)
# imgList = []
# studentIds = []
# for path in pathList:
#     imgList.append(cv2.imread(os.path.join(folderPath, path)))
#     studentIds.append(os.path.splitext(path)[0])
#
#     fileName = f'{folderPath}/{path}'
#     bucket = storage.bucket()
#     blob = bucket.blob(fileName)
#     blob.upload_from_filename(fileName)
#
#
#     # print(path)
#     # print(os.path.splitext(path)[0])
# print(studentIds)
#
#
# def findEncodings(imagesList):
#     encodeList = []
#     for img in imagesList:
#         img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
#         encode = face_recognition.face_encodings(img)[0]
#         encodeList.append(encode)
#
#     return encodeList
#
#
# print("Encoding Started ...")
# encodeListKnown = findEncodings(imgList)
# encodeListKnownWithIds = [encodeListKnown, studentIds]
# print("Encoding Complete")
#
# file = open("EncodeFile.p", 'wb')
# pickle.dump(encodeListKnownWithIds, file)
# file.close()
# print("File Saved")