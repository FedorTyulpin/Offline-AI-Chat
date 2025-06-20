
try:
    import ollama
    import tkinter as tk
    from tkinter import *
except ModuleNotFoundError as err:
    module = str(err).split("'")[1]

    exit(f"{err}, try '\033[34mpip install {module}\033[0m'")



downloaded_modules = [x["model"] for x in ollama.list().models]




class AI_chat():
    def __init__(self, model, label, history=None):

        if model in downloaded_modules:
            self.model = model
        else: exit(f"This model: \033[1m\033[34m{model}\033[0m is not installed. check if you have written the name correctly, if yes, then use the command '\033[34mollama run {model}\033[0m'")
        self.label = label
        self.history = [] if history is None else history

    def text_query(self, text : str, is_thinking : bool =False) -> str:
        # Добавляем сообщение в историю
        self.history.append({"role": "user", "content": text})

        # Формируем запрос с историей диалога
        response = ollama.chat(
            model=self.model,
            messages=self.history,
            stream=False,  # Для поточного вывода установите True
            think= is_thinking
        )

        # Получаем ответ модели
        ai_response = response['message']['content']
        self.history.append({"role": "assistant", "content": ai_response})
        return f"{ai_response}"



