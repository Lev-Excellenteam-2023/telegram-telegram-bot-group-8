import asyncio
from chatgpt_interface.openai_api  import OpenAIChatAPI


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
    message = {"role": "system", "content": f"Please provide a concise response: Is the answer relevant? (Yes/No)\n\nQuestion: {question}\nAnswer: {answer}\n"}
    response = await chat.generate_response([message])
    return response.lower() == 'yes'





async def calculate_scores1(chat: OpenAIChatAPI, questions_and_answers):
    """
    Calculates scores for doctor's behavior and professionalism based on patient feedback.

    Args:
        chat (OpenAIChatAPI): An instance of the OpenAIChatAPI class for communication with OpenAI.
        questions_and_answers (list): A list of tuples, each containing a question and its corresponding answer.

    Returns:
        str: A comma-separated string of responses (positive/neutral/negative).
    """
    score = 0
    responses = []
    for question, answer in questions_and_answers.items():
        responses.append("Question: " + question + " Answer: " + answer)

    # Ask ChatGPT about relevance and polarity for all responses
    combined_responses = ", ".join(responses)
    prompt = f"Tell me what the patient's scores are for the doctor according to the following questions and answers. " \
             f"Provide responses in the order: positive/neutral/negative for each question.\n\n" \
             f"Questions and Answers:\n{combined_responses}\n"
    response = await chat.generate_response(prompt)

    for ans_score in response.strip("/"):
        if ans_score == "positive":
            score += 10
        elif ans_score == "neutral":
            score += 5
        elif ans_score == "negative":
            score -= 0

    # Construct the final response
    treatment_score = score / len(questions_and_answers)
    return treatment_score
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
    messages=[]
    questions_and_answers_string =''
    for question, answer in questions_and_answers.items():
        questions_and_answers_string+='question: '+question
        questions_and_answers_string+='answer: '+answer
        # Ask ChatGPT about relevance and polarity
    prompt = f"Tell me what the patient's score is for the doctor according to the question and answer below,\
notice to write in one word for each question your opinion and just from the follow options (positive/negative/neutral)\
write it for each question in space between them .for example like that: positive negative neutral negative positive"
    messages.append( {"role": "system", "content": prompt})
    await chat.generate_response(messages)
    messages.append({"role": "user", "content": questions_and_answers_string})
    response = await chat.generate_response(messages)
    responses=response.split()
    for i in responses:
        if i == "positive":
            score += 10
        elif i == "neutral":
            score += 5
        elif i == "negative":
            score -= 0

    # Construct the final response
    treatment_score = score / len(questions_and_answers)
    return treatment_score
