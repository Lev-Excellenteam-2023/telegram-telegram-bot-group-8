import firebase_admin
from firebase_admin import credentials
from faker import Faker

cred = credentials.Certificate("doctors-feedbacks-firebase-adminsdk-tgu9x-3a67938c9e.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://doctors-feedbacks-default-rtdb.firebaseio.com'
})

from firebase_admin import db

# Reference to the root of your database
ref = db.reference('/')

def insert_doctor(first_name,last_name):
    new_data_ref = ref.child('doctors').push({
        'first name': first_name,
        'last name': last_name,
    })

# Generate and insert 80 doctors with different names
fake = Faker()
for _ in range(80):
    first_name = fake.first_name()
    last_name = fake.last_name()
    insert_doctor(first_name, last_name)

#print('New data key:', new_data_ref.key)

