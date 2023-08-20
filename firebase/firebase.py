import firebase_admin
from firebase_admin import credentials
import os
from firebase_admin import db
from faker import Faker

cred = credentials.Certificate(os.getenv("FIREBASE_JSON"))
firebase_admin.initialize_app(cred, {
    'databaseURL': os.getenv("DATABASE_URL")
})

# Reference to the root of your database
ref = db.reference('/')


def insert_doctor(first_name, last_name):
    new_data_ref = ref.child('doctors').push({
        'first name': first_name,
        'last name': last_name,
        'score': 0
    })


def insert_feedbacks(first_name, last_name, answers_list, score):
    # Query the doctor based on first_name and last_name
    doctors_ref = ref.child('doctors')
    query = doctors_ref.order_by_child('first name').equal_to(first_name).get()
    matching_doctors = [doctor_id for doctor_id, doctor_data in query.items() if
                        doctor_data.get('last name') == last_name]

    if matching_doctors:
        doctor_id = matching_doctors[0]  # Assume there's only one doctor with the given name
        feedbacks_ref = doctors_ref.child(doctor_id).child('feedbacks')

        new_feedback_ref = feedbacks_ref.push()
        feedback_id = new_feedback_ref.key
        answers_ref = new_feedback_ref.child('answers')

        for i, answer in enumerate(answers_list):
            answer_id = f'answer_{i + 1}'
            answers_ref.child(answer_id).set(answer)

        print('New feedback key:', feedback_id)

        # Update the doctor's score
        current_score = get_doctor_score(first_name, last_name)
        if current_score is not None:
            feedbacks_count = len(feedbacks_ref.get())
            new_score = (current_score * (feedbacks_count - 1) + int(score)) / feedbacks_count
            doctors_ref.child(doctor_id).update({'score': new_score})
            print('Doctor score updated:', new_score)
    else:
        print('No matching doctor found.')


def get_doctor_score(first_name, last_name):
    doctors_ref = ref.child('doctors')
    query = doctors_ref.order_by_child('first name').equal_to(first_name).get()
    matching_doctors = [doctor_id for doctor_id, doctor_data in query.items() if
                        doctor_data.get('last name') == last_name]

    if matching_doctors:
        doctor_id = matching_doctors[0]  # Assume there's only one doctor with the given name
        doctor_data = doctors_ref.child(doctor_id).get()
        return doctor_data.get('score', 0)
    else:
        return None


def get_feedbacks_for_doctor(first_name, last_name):
    # Initialize the Firebase Admin SDK and database reference
    # (Make sure you've already initialized the SDK and have the database reference 'ref' available)

    # Query the doctor based on first_name and last_name
    query = ref.child('doctors').order_by_child('first name').equal_to(first_name).get()
    matching_doctors = [doctor_id for doctor_id, doctor_data in query.items() if
                        doctor_data.get('last name') == last_name]

    feedbacks = []

    if matching_doctors:
        doctor_id = matching_doctors[0]  # Assume there's only one doctor with the given name
        feedbacks_ref = ref.child('doctors').child(doctor_id).child('feedbacks')

        # Iterate through the feedbacks and retrieve the feedback data
        for feedback_id, feedback_data in feedbacks_ref.get().items():
            feedbacks.append(feedback_data.get('answers', {}))

    return feedbacks


def get_all_doctors():
    doctors_ref = ref.child('doctors')
    doctors_list = doctors_ref.get()

    all_doctors = []
    if doctors_list:
        for doctor_id, doctor_data in doctors_list.items():
            all_doctors.append(doctor_data)

    return all_doctors

# Generate and insert 80 doctors with different names
# fake = Faker()
# for _ in range(80):
#   first_name = fake.first_name()
#  last_name = fake.last_name()
# insert_doctor(first_name, last_name)

# print('New data key:', new_data_ref.key)
