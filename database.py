import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://facerecognition-47b6a-default-rtdb.firebaseio.com/"
})

ref = db.reference('Students')

data = {
    "0":
        {
            "name": "Murtaza Hassan",
            "major": "Robotics",
            "total_attendance": 7,
            "last_attendance_time": "2022-12-11 00:54:34"
        },
    "1":
        {
            "name": "Emly Blunt",
            "major": "Economics",
            "total_attendance": 12,
            "last_attendance_time": "2022-12-11 00:54:34"
        },
    "2":
        {
            "name": "Elon Musk",
            "major": "Physics",
            "total_attendance": 7,
            "last_attendance_time": "2022-12-11 00:54:34"
        }
}

for key, value in data.items():
    ref.child(key).set(value)











# import firebase_admin
# from firebase_admin import credentials, db
#
# cred = credentials.Certificate("serviceAccountKey.json")
# firebase_admin.initialize_app(cred, {
#     'databaseURL': 'https://facerecognition-47b6a-default-rtdb.firebaseio.com/'
# })
#
# ref = db.reference('students')
#
# data = {
#     '0': {
#         'name': 'jobs',
#         'last_attendance_time': '2022-12-11 00:54:34',
#         'major': 'CSE',
#         'total_attendance': 7
#     },
#     '1': {
#         'name': 'emily blunt',
#         'last_attendance_time': '2022-12-11 00:54:34',
#         'major': 'CSE',
#         'total_attendance': 10
#     },
#     '2': {
#         'name': 'elon musk',
#         'last_attendance_time': '2022-12-11 00:54:34',
#         'major': 'CSE',
#         'total_attendance': 13
#     },
#     '3': {
#         'name': 'tesla',
#         'last_attendance_time': '2022-12-11 00:54:34',
#         'major': 'CSE',
#         'total_attendance': 16
#     }
# }
#
# for key, value in data.items():
#     ref.child(key).set(value)
# #