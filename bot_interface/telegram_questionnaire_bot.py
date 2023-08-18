import os

import requests
from flask import Flask, request, Response


TELEGRAM_INIT_WEBHOOK_URL = f'{os.getenv("BASE_URL")}{os.getenv("TOKEN")}/{os.getenv("SETWEBHOOK")}/message'
requests.get(TELEGRAM_INIT_WEBHOOK_URL)

intro_message=r'Hello there! We hope you\'re feeling well after your recent medical treatment. Your feedback matters a lot to us!\
We\'d like to kindly request a few moments of your time to answer a few questions about your experience. Your responses will help us ensure the best care for you and other patients in the future.\
By sharing your thoughts, you\'re not only helping us improve, but you\'re also contributing to the well-being of our community.\
As a thank you, you\'ll be able to enjoy personalized recommendations for highly recommended doctors whenever you need assistance in the future. Your valuable input truly makes a difference.\
To get started, simply reply with your answers to the following questions. Remember, your feedback is a gift that helps us grow and provide even better care.\
Thank you for being a part of our mission to deliver exceptional healthcare. Let\'s begin!'


fill = {}
current_question_index = {}
if_in_name_of_doctor={}

app = Flask(__name__)

def name_of_doctor_function(chat_id):
    message='enter the doctor first name and last name'
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
        send_message(chat_id,questions[current_question_index[chat_id]])
        current_question_index[chat_id] += 1
    else:
        fill[chat_id] = False
        send_message(chat_id, "Thank you for answering all questions!")
        chat_id_finish.append(chat_id)



@app.route('/message', methods=["POST"])
def handle_message():
    global fill
    global current_question_index
    data = request.get_json()
    chat_id = data['message']['chat']['id']
    message_text = data['message']['text']
    if message_text=='/start':
        if chat_id not in user_answers:
            send_message(chat_id, intro_message)
            name_of_doctor_function(chat_id)
        else:
            response="can't start new questionnaire in a middle of questionnaire. please answer the question\n"
            current_question_index[chat_id] =current_question_index[chat_id]- 1
            send_message(chat_id, response)
            send_next_question(chat_id)
    elif chat_id in if_in_name_of_doctor and if_in_name_of_doctor[chat_id]==True:
        name_of_doctor[chat_id]=message_text
        if_in_name_of_doctor[chat_id] = False
        start_questionnaire(chat_id)
    elif chat_id in fill and fill[chat_id] and current_question_index[chat_id] - 1 < len(questions):
        user_answers[chat_id][current_question_index[chat_id] - 1] = message_text
        send_next_question(chat_id)
    else:
        response = "Unknown command. Please use /start to begin."
        send_message(chat_id, response)

    return Response("success")

def send_message(chat_id, text):
    send_url = f'https://api.telegram.org/bot{os.getenv("TOKEN")}/sendMessage'
    payload = {'chat_id': chat_id, 'text': text}
    requests.get(send_url, params=payload)



app.run(port=5002)

#if __name__=="__main__":
 #   main()