import os

import requests
import firebase.firebase
from flask import Flask, request, Response
from bot_interface.global_variables import chat_id_finish, name_of_doctor, user_answers, questions
import chatgpt_interface.chat_gpt_client
from chatgpt_interface.openai_api import SyncOpenAIChatAPI

openai_chat = SyncOpenAIChatAPI()

TELEGRAM_INIT_WEBHOOK_URL = 'https://api.telegram.org/bot{}/setWebhook?url=https://9115-2-54-50-39.ngrok-free.app/message'.format(
    '6522625279:AAFUI73YuVL079FfCw0pKAGy0ir9uuCDu_w')
requests.get(TELEGRAM_INIT_WEBHOOK_URL)

intro_message = r'Hello there! We hope you\'re feeling well after your recent medical treatment. Your feedback matters a lot to us!\
We\'d like to kindly request a few moments of your time to answer a few questions about your experience. Your responses will help us ensure the best care for you and other patients in the future.\
By sharing your thoughts, you\'re not only helping us improve, but you\'re also contributing to the well-being of our community.\
As a thank you, you\'ll be able to enjoy personalized recommendations for highly recommended doctors whenever you need assistance in the future. Your valuable input truly makes a difference.\
To get started, simply reply with your answers to the following questions. Remember, your feedback is a gift that helps us grow and provide even better care.\
Thank you for being a part of our mission to deliver exceptional healthcare. Let\'s begin!'

fill = {}
current_question_index = {}
if_in_name_of_doctor = {}
registered_users = []
app = Flask(__name__)


def name_of_doctor_function(chat_id):
    message = 'enter the doctor first name and last name'
    if_in_name_of_doctor[chat_id] = True
    send_message(chat_id, message)


# Helper function to start the questionnaire
def start_questionnaire(chat_id):
    user_answers[chat_id] = {}
    current_question_index[chat_id] = 0
    fill[chat_id] = True
    send_next_question(chat_id)


# Helper function to send the next question
def send_next_question(chat_id):
    if current_question_index[chat_id] < len(questions):
        send_message(chat_id, questions[current_question_index[chat_id]])
        current_question_index[chat_id] += 1
    else:
        fill[chat_id] = False
        send_message(chat_id, "Thank you for answering all questions!")
        chat_id_finish.append(chat_id)
        if chat_id not in registered_users:
            registered_users.append(chat_id)


def send_doctor_feedbacks(chat_id, doctor_first_name, doctor_last_name):
    feedbacks = firebase.firebase.get_feedbacks_for_doctor(doctor_first_name, doctor_last_name)
    if feedbacks:
        response = "Feedbacks for Doctor {} {}:\n\n".format(doctor_first_name, doctor_last_name)
        for feedback in feedbacks:
            response += "\n".join(["- " + answer for answer in feedback.values()])
            response += "\n\n"
        send_message(chat_id, response)
    else:
        send_message(chat_id, "No feedbacks found for Doctor {} {}.".format(doctor_first_name, doctor_last_name))


def send_doctor_report(chat_id, doctor_first_name, doctor_last_name):
    # Fetch feedbacks for the specified doctor using your database interaction methods
    feedbacks = firebase.firebase.get_feedbacks_for_doctor(doctor_first_name, doctor_last_name)

    if feedbacks:
        # Calculate scores and generate detailed report using your existing functions
        report = chatgpt_interface.chat_gpt_client.generate_doctor_report(openai_chat, feedbacks, questions)
        send_message(chat_id, report)
    else:
        send_message(chat_id, "No feedbacks found for Doctor {} {}.".format(doctor_first_name, doctor_last_name))


def get_best_doctors(chat_id):
    # Get the list of doctors from your database
    doctors_list = firebase.firebase.get_all_doctors()  # Replace with your database retrieval method

    if not doctors_list:
        send_message(chat_id, "No doctors found.")
        return

    best_doctors = []
    for doctor_data in doctors_list:
        doctor_score = doctor_data.get('score', 0)
        if doctor_score >= 9:
            best_doctors.append(doctor_data)

    if not best_doctors:
        send_message(chat_id, "No doctors with a score of 9 or higher found.")
        return

    response = "Doctors with the best feedback:\n\n"
    for doctor in best_doctors:
        doctor_name = f"{doctor.get('first name')} {doctor.get('last name')}"
        response += f"- {doctor_name}\n"

    send_message(chat_id, response)


@app.route('/message', methods=["POST"])
def handle_message():
    global fill
    global current_question_index
    data = request.get_json()
    chat_id = data['message']['chat']['id']
    message_text = data['message']['text']
    if message_text == '/start':
        if chat_id not in user_answers:
            send_message(chat_id, intro_message)
            name_of_doctor_function(chat_id)
        else:
            response = "can't start new questionnaire in a middle of questionnaire. please answer the question\n"
            current_question_index[chat_id] = current_question_index[chat_id] - 1
            send_message(chat_id, response)
            send_next_question(chat_id)
    elif chat_id in if_in_name_of_doctor and if_in_name_of_doctor[chat_id] == True:
        name_of_doctor[chat_id] = message_text
        if_in_name_of_doctor[chat_id] = False
        start_questionnaire(chat_id)
    elif chat_id in fill and fill[chat_id] and current_question_index[chat_id] - 1 < len(questions):
        user_answers[chat_id][current_question_index[chat_id] - 1] = message_text
        send_next_question(chat_id)
    elif chat_id in registered_users:
        if message_text.startswith('/view_feedback'):
            params = message_text.split()[1:]
            if len(params) == 2:
                doctor_first_name, doctor_last_name = params
                send_doctor_feedbacks(chat_id, doctor_first_name, doctor_last_name)
            else:
                response = "Invalid command. Usage: /view_feedbacks <Doctor's First Name> <Doctor's Last Name>"
                send_message(chat_id, response)
    elif message_text.startswith('/generate_report'):
        params = message_text.split()[1:]
        if len(params) == 2:
            doctor_first_name, doctor_last_name = params
            send_doctor_report(chat_id, doctor_first_name, doctor_last_name)
        else:
            response = "Invalid command. Usage: /generate_report <Doctor's First Name> <Doctor's Last Name>"
            send_message(chat_id, response)
    elif message_text == '/best_doctors':
        get_best_doctors(chat_id)

    else:
        response = "Unknown command. Please use /start to begin."
        send_message(chat_id, response)

    return Response("success")


def send_message(chat_id, text):
    send_url = 'https://api.telegram.org/bot{}/sendMessage'.format('6522625279:AAFUI73YuVL079FfCw0pKAGy0ir9uuCDu_w')
    payload = {'chat_id': chat_id, 'text': text}
    requests.get(send_url, params=payload)


def start_flask_server():
    app.run(port=5002)
