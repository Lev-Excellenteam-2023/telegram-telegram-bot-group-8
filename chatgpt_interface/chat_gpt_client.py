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
