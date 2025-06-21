
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
        default_model = downloaded_modules[0]

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
    def __init__(self,  label, model=None, history=None):
        if model is not None:
            if model in downloaded_modules:
                self.model = model
        else:
            self.model = default_model

        self.label = label
        self.history = [] if history is None else history

    def text_query(self, text: str, is_thinking: bool = False) -> str:
        # Добавляем блокировку для безопасного доступа к истории
        with request_lock:
            self.history.append({"role": "user", "content": text})

            try:
                response = ollama.chat(
                    model=self.model,
                    messages=self.history,
                    stream=False,
                    think=is_thinking
                )

                ai_response = response['message']['content']
                self.history.append({"role": "assistant", "content": ai_response})
                return f"{ai_response}"
            except Exception as e:
                # В случае ошибки возвращаем сообщение и не сохраняем в историю
                return f"⚠️ Error: {str(e)}"



