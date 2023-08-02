import os
from dotenv import load_dotenv
import flet as ft

import openai


def main():
    ENV_FILE = "../.env"
    env_loaded = load_dotenv(ENV_FILE)
    if not env_loaded:
        exit(f"Не удалось прочитать переменные окружения в файле: {ENV_FILE}")
    ft.app(target=window, view=ft.WEB_BROWSER)


def window(page: ft.page.Page):
    page.scroll = ft.page.ScrollMode.ADAPTIVE
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    question = ft.TextField(label="Вопрос:", value="Можно ли считать эти два навыка дубликатами?", width=600)
    skill_1 = ft.TextField(label="Навык 1", autofocus=True, width=600)
    skill_2 = ft.TextField(label="Навык 2", width=600)
    greetings = ft.Column()
    row = ft.Row(controls=[skill_1, skill_2], spacing=0, alignment=ft.MainAxisAlignment.CENTER)

    def btn_click(event):
        text = f'{question.value.replace("?", "")} "{skill_1.value}" и "{skill_2.value}" ?'

        greetings.controls.append(ft.Text(f"Вопрос: {text}", size=22))
        greetings.controls.append(ft.Text(f"Ответ: {get_answer(text)}", size=22))
        skill_1.value = ""
        skill_2.value = ""
        page.update()
        skill_1.focus()

    btn_start = ft.ElevatedButton("Спросить", on_click=btn_click)
    page.add(
        question,
        row,
        btn_start,
        greetings,
    )


def get_answer(question: str) -> str:
    SECRET =os.getenv("GPT_TOKEN")
    openai.api_key = SECRET
    MODEL = "gpt-3.5-turbo"
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
    answers = [i["message"]["content"] for i in response["choices"]]
    return answers[0]


if name == 'main':
    main()
