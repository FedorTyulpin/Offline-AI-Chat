'''
*/AI.py
file for AI logic
'''
try:
    import ollama
    import tkinter as tk
    from tkinter import *
    from tkinter import ttk
    import threading
    request_lock = threading.Lock()

except ModuleNotFoundError as err:
    module = str(err).split("'")[1]

    exit(f"{err}, try '\033[34mpip install {module}\033[0m'")



downloaded_modules = [x["model"] for x in ollama.list().models]


if not [x for x in open("meta/model.txt")]:
    modelTxt = open("meta/model.txt",mode="w+")
    if len(downloaded_modules) == 1:
        modelTxt.write(downloaded_modules[0])

    elif len(downloaded_modules)>1:
        root = Tk()
        root.title("Выбрать модель")

        ttk.Label(text="chose model that you want use:").grid()
        com = ttk.Combobox(values=downloaded_modules,state='readonly')
        com.grid()

        accept_btn = ttk.Button(text= "accept", command=lambda : (modelTxt.write(com.get()),root.destroy()))
        accept_btn.grid()
        root.mainloop()

    else:
        raise ""
    modelTxt.close()

default_model = [x for x in open("meta/model.txt")][0]





class AI_chat():
    def __init__(self,  label: str, model: str | None = None, history: list[dict] | None = None) -> None:
        if model is not None:
            if model in downloaded_modules:
                self.model = model
        else:
            self.model = default_model

        self.label = label
        self.history = [] if history is None else history

    def stream_query(self, text: str, callback, is_thinking: bool = True) -> str:
        """Потоковый запрос с callback для обновления в реальном времени"""
        # Добавляем сообщение пользователя в историю
        self.history.append({"role": "user", "content": text})

        # Создаем потоковый запрос
        stream = ollama.chat(
            model=self.model,
            messages=self.history,
            think=None if is_thinking else False,
            stream=True,  # Включаем потоковый вывод
            keep_alive= True
        )

        full_response = ""
        for chunk in stream:
            if 'message' in chunk and 'content' in chunk['message']:
                content_chunk = chunk['message']['content']
                full_response += content_chunk
                # Вызываем callback для каждой новой части ответа
                callback(content_chunk)

        # Добавляем полный ответ в историю
        self.history.append({"role": "assistant", "content": full_response})
        return full_response



