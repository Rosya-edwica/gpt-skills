import os
import openai
from models import Pair
from dotenv import load_dotenv

env_loaded = load_dotenv("../.env")

openai.api_key = os.getenv("GPT_TOKEN")
MODEL = "gpt-3.5-turbo"


def check_skills_similarity(pair: Pair) -> bool | None:
    """Если навыки похожи, вернется True, иначе False"""

    question = f"Можно ли считать эти навыки дубликатами: '{pair.Skill1}' и '{pair.Skill2}'? Ответь Да или Нет."
    try:
        response = openai.ChatCompletion.create(
            model=MODEL,
            messages=[
                {
                    "role": "system",
                    "content": question,
                },
            ],
            temperature=0,
        )
        return send_answer(response)
    except BaseException as err:
        print(f"Произошла ошибка: {err}")
        return None


def send_answer(gpt_response: dict) -> bool:
    answers = [i["message"]["content"] for i in gpt_response["choices"]]
    match answers[0].replace(".", "").lower():
        case "да":
            return True
        case "нет":
            return False
