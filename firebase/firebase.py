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
        'score':0
    })
def insert_feedbacks(first_name, last_name, feedbacks_list,score):
    # Query the doctor based on first_name and last_name
    doctors_ref = ref.child('doctors')
    query = doctors_ref.order_by_child('first name').equal_to(first_name).get()
    matching_doctors = [doctor_id for doctor_id, doctor_data in query.items() if doctor_data.get('last name') == last_name]

    if matching_doctors:
        doctor_id = matching_doctors[0]  # Assume there's only one doctor with the given name
        feedbacks_ref = doctors_ref.child(doctor_id).child('feedbacks')

        for feedback in feedbacks_list:
            feedback_data = {'answers': feedback}
            new_feedback_ref = feedbacks_ref.push(feedback_data)
            print('New feedback key:', new_feedback_ref.key)

        # Update the doctor's score
        current_score = get_doctor_score(first_name, last_name)
        if current_score is not None:
            new_score = current_score + int(score)
            doctors_ref.child(doctor_id).update({'score': new_score})
            print('Doctor score updated:', new_score)
    else:
        print('No matching doctor found.')

def get_doctor_score(first_name, last_name):
    doctors_ref = ref.child('doctors')
    query = doctors_ref.order_by_child('first name').equal_to(first_name).get()
    matching_doctors = [doctor_id for doctor_id, doctor_data in query.items() if doctor_data.get('last name') == last_name]

    if matching_doctors:
        doctor_id = matching_doctors[0]  # Assume there's only one doctor with the given name
        doctor_data = doctors_ref.child(doctor_id).get()
        return doctor_data.get('score', 0)
    else:
        return None


# Generate and insert 80 doctors with different names
#fake = Faker()
#for _ in range(80):
 #   first_name = fake.first_name()
  #  last_name = fake.last_name()
   # insert_doctor(first_name, last_name)

#print('New data key:', new_data_ref.key)

