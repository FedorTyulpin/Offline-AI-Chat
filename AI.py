
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
if not downloaded_modules: 
    raise "No downloaded models exist"

if not [x for x in open("meta/model.txt")]:
    modelTxt = open("meta/model.txt",mode="w+") 

    if len(downloaded_modules) == 1:
        modelTxt.write(downloaded_modules[0])
    else:
        root = Tk()
        root.title("Выбрать модель") #!!!

        ttk.Label(text="chose model that you want use:").grid()
        com = ttk.Combobox(values=downloaded_modules,state='readonly')
        com.grid()

        accept_btn = ttk.Button(text= "accept", command=lambda : (modelTxt.write(com.get()),root.destroy()))
        accept_btn.grid()
        root.mainloop()
    
    modelTxt.close() 


default_model = [x for x in open("meta/model.txt")][0]




class AI_chat:
    """
    AI chat. Based on the model from `meta/model.txt`

    Parameters:
    label: The name of the chat room
    model: Model from `meta/model.txt`
    history: Additional pre-prepared history
    """
    def __init__(self,  label: str, model: str = None, history: list[dict[str,str]] = None) -> None:
        if model is not None:
            if model in downloaded_modules:
                self.model = model
        else:
            self.model = default_model

        self.label = label
        self.history = [] if history is None else history

    def stream_query(self, text: str, callback, is_thinking: bool) -> str:
        """Streaming request with callback for real-time update"""
        self.history.append({"role": "user", "content": text})

        stream = ollama.chat(
            model=self.model,
            messages=self.history,
            think=None if is_thinking else False,
            stream=True
        )

        full_response = ""
        for chunk in stream:
            if 'message' in chunk and 'content' in chunk['message']:
                content_chunk = chunk['message']['content']
                full_response += content_chunk
                callback(content_chunk)

        self.history.append({"role": "assistant", "content": full_response})
        return full_response



