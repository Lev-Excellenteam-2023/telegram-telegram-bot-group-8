import asyncio
from openai_api import OpenAIChatAPI


async def is_answer_relevant(chat: OpenAIChatAPI, question: str, answer: str) -> bool:
    """
    Determines whether an answer to a given question is relevant using the OpenAIChatAPI.

    Args:
        chat (OpenAIChatAPI): An instance of the OpenAIChatAPI class for communication with OpenAI.
        question (str): The question for which the answer's relevance needs to be assessed.
        answer (str): The answer to be evaluated for relevance.

    Returns:
        bool: True if the answer is relevant, False otherwise.
    """
    prompt = f"Please provide a concise response: Is the answer relevant? (Yes/No)\n\nQuestion: {question}\nAnswer: {answer}\n"
    response = await chat.generate_response(prompt)
    return response.lower() == 'yes'


async def calculate_scores(chat: OpenAIChatAPI, questions_and_answers):
    """
    Calculates scores for doctor's behavior and professionalism based on patient feedback.

    Args:
        chat (OpenAIChatAPI): An instance of the OpenAIChatAPI class for communication with OpenAI.
        questions_and_answers (list): A list of tuples, each containing a question and its corresponding answer.

    Returns:
        str: A string representing the calculated scores in a specific format.
    """
    score = 0
    for question, answer in questions_and_answers:
        # Ask ChatGPT about relevance and polarity
        prompt = f"Tell me what the patient's score is for the doctor according to the question and answer below, " \
                 f"notice to write in one word your opinion and just from the follow options (positive/negative/neutral) of the " \
                 f"\n\nQuestion: {question}\nAnswer: {answer}\n"
        response = chat.generate_response(prompt)
        if response == "positive":
            score += 10
        elif response == "neutral":
            score += 5
        elif response == "negative":
            score -= 10

    # Construct the final response
    treatment_score = f"Score: {score / len(questions_and_answers)}"
    return treatment_score


def generate_doctor_report(chat_api: OpenAIChatAPI, feedbacks: list):
    """
    Generate a detailed report about the doctor based on provided feedback.

    Args:
        chat (OpenAIChatAPI): An instance of the OpenAIChatAPI class for communication with OpenAI.
        feedbacks (list): A list of feedbacks, where each feedback is a list of tuples
                         containing questions and answers.

    Returns:
        str: A detailed report about the doctor based on the provided feedback.
    """
    prompt = "Generate a detailed report about the doctor based on the provided feedback:\n\n"

    for i, feedback in enumerate(feedbacks, start=1):
        prompt += f"Feedback {i}:\n"
        for question, answer in feedback:
            prompt += f"Question: {question}\n"
            prompt += f"Answer: {answer}\n"
        prompt += "\n"

    prompt += "Please provide a detailed report about the doctor considering the feedback provided above."
    report = asyncio.run(chat_api.generate_response(prompt))
    return report
