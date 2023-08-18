import threading
import chatgpt_interface.chat_gpt_client
from chatgpt_interface.openai_api import OpenAIChatAPI
import asyncio
import firebase.firebase
import bot_interface.global_variables
import bot_interface.telegram_questionnaire_bot

async def main():
    openai_chat = OpenAIChatAPI()
    while True:
        users_finish=list(bot_interface.global_variables.chat_id_finish)
        if len(users_finish)>0:
            for chat_id in users_finish:
                questions_and_answers={}
                answers= bot_interface.global_variables.user_answers[chat_id]
                for i,question in enumerate(bot_interface.global_variables.questions):
                    questions_and_answers[question]=answers[i]
                score=await chatgpt_interface.chat_gpt_client.calculate_scores(openai_chat, questions_and_answers)
                print(score)
                bot_interface.global_variables.chat_id_finish.remove(chat_id)
                del bot_interface.global_variables.user_answers[chat_id]
                list_of_answers=[]
                for i in range(len(answers)):
                    list_of_answers.append(answers[i])
                firebase.firebase.insert_feedbacks(bot_interface.global_variables.name_of_doctor[chat_id].split()[0],\
                                          bot_interface.global_variables.name_of_doctor[chat_id].split()[1],\
                                          list_of_answers,score)






if __name__ == "__main__":
    # Create and start the Flask server thread
    server_thread = threading.Thread(target= bot_interface.telegram_questionnaire_bot.start_flask_server)
    server_thread.start()

    # Run the main function in the asyncio event loop
    asyncio.run(main())

    # Wait for the server thread to finish
    server_thread.join()