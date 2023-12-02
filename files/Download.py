import pandas as pd
import firebase_admin
from firebase_admin import db, credentials
from datetime import datetime
import os

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://minorproject-f2572-default-rtdb.firebaseio.com/'
})

students = db.reference(f'Students').get()
ids = [i for i in range(1, len(students))]
names = [students[i]['name'] for i in range(1, len(students))]
total_attendance = [students[i]['total_attendance'] for i in range(1, len(students))]

dic = {'id': ids, 'name': names, 'total_attendance': total_attendance}

df = pd.DataFrame(dic)

date = datetime.now().strftime("%Y-%m-%d")

path = r'C:\Users\annas\Downloads'
filename = f'attendance[{date}].xlsx'

df.to_excel(os.path.join(path, filename))
