import chatgpt_interface.chat_gpt_client
from chatgpt_interface.openai_api import OpenAIChatAPI
from bot_interface import telegram_questionnaire_bot
import asyncio
import firebase

async def main():
    openai_chat = OpenAIChatAPI()
    while True:
        users_finish=list(telegram_questionnaire_bot.chat_id_finish)
        if len(users_finish)>0:
            for chat_id in users_finish:
                questions_and_answers={}
                answers= telegram_questionnaire_bot.user_answers[chat_id]
                for i,question in enumerate(telegram_questionnaire_bot.questions):
                    questions_and_answers[question]=answers[i]
                score=await chatgpt_interface.chat_gpt_client.calculate_scores(openai_chat, questions_and_answers)
                print(score)
                telegram_questionnaire_bot.chat_id_finish.remove(chat_id)
                del telegram_questionnaire_bot.user_answers[chat_id]
                list_of_answers=[]
                for i in range(len(answers)):
                    list_of_answers.append(answers[i])
                firebase.insert_feedbacks(telegram_questionnaire_bot.doctors_names[chat_id].split()[0],\
                                          telegram_questionnaire_bot.doctors_names[chat_id].split()[1],\
                                          list_of_answers,score)








if __name__ == "__main__":
    asyncio.run(main())
