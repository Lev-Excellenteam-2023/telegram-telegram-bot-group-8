import requests
from flask import Flask, request, Response
import keys


TELEGRAM_INIT_WEBHOOK_URL = f'{keys.BASE_URL}{keys.TOKEN}/{keys.SETWEBHOOK}/message'
requests.get(TELEGRAM_INIT_WEBHOOK_URL)
questions = ['How would you describe the dentist\'s demeanor and attitude towards you during the visit?',
'how likely are you to recommend this dentist to a friend or family member?',
'How well did the dentist manage your pain and discomfort during the treatment?',
'How would you rate the dentist\'s knowledge and expertise in the field of dentistry?',
'Did the dentist follow proper hygiene and safety protocols during your visit?']

intro_message=r'Hello there! We hope you\'re feeling well after your recent medical treatment. Your feedback matters a lot to us!\
We\'d like to kindly request a few moments of your time to answer a few questions about your experience. Your responses will help us ensure the best care for you and other patients in the future.\
By sharing your thoughts, you\'re not only helping us improve, but you\'re also contributing to the well-being of our community.\
As a thank you, you\'ll be able to enjoy personalized recommendations for highly recommended doctors whenever you need assistance in the future. Your valuable input truly makes a difference.\
To get started, simply reply with your answers to the following questions. Remember, your feedback is a gift that helps us grow and provide even better care.\
Thank you for being a part of our mission to deliver exceptional healthcare. Let\'s begin!'

chat_id_finish=[]
user_answers = {}  # Store answers for each user
app = Flask(__name__)
fill = {}
current_question_index = {}


# Helper function to start the questionnaire
def start_questionnaire(chat_id):
    user_answers[chat_id] = {}
    current_question_index[chat_id] = 0
    fill[chat_id] = True
    send_message(chat_id, intro_message)
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



@app.route('/message', methods=["POST"])
def handle_message():
    global fill
    global current_question_index
    data = request.get_json()
    chat_id = data['message']['chat']['id']
    message_text = data['message']['text']

    if chat_id not in user_answers:
        start_questionnaire(chat_id)
    elif fill[chat_id] and current_question_index[chat_id] - 1 < len(questions):
        user_answers[chat_id][current_question_index[chat_id] - 1] = message_text
        send_next_question(chat_id)
    else:
        response = "Unknown command. Please use /start to begin."
        send_message(chat_id, response)

    return Response("success")

def send_message(chat_id, text):
    send_url = f'https://api.telegram.org/bot{keys.TOKEN}/sendMessage'
    payload = {'chat_id': chat_id, 'text': text}
    requests.get(send_url, params=payload)

app.run(port=5002)
