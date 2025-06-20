import os

import tkinter as tk
from tkinter import *
from tkinter import scrolledtext, messagebox, simpledialog
from tkinter.messagebox import askyesno



import AI
import metaGenerator


class AIchatAPP:

    def __init__(self, root):

        self.chats = {}
        self.chosen_chat = None


        self.chat_panel = tk.scrolledtext.ScrolledText()
        self.root = root
        self.root.title("DeepSeek Chat")
        self.root.minsize(800, 500)
        self.root.maxsize(1000,700)



        self.main_panel()
        self.side_panel()


    def side_panel(self):

        self.side = LabelFrame(self.root,text="Чаты")
        self.side.grid(row=0, column=0,ipadx=5, ipady=5,sticky=NS)

        new_chat_btn = Button(self.side, text="+ new chat",command=lambda : self.create_chat())
        new_chat_btn.grid(columnspan=3,sticky="we")

        chats_list = [i[:-4] for i in os.listdir("meta/chats")]

        for chat_id in range(len(chats_list)):
            current_chat = chats_list[chat_id]  # Сохраняем значение для этой итерации

            self.chats[current_chat] = AI.AI_chat("deepseek-r1:latest", current_chat, metaGenerator.load(current_chat))

            Button(
                self.side,
                text=current_chat if len(current_chat)<= 10 else current_chat[:7]+"...",
                command=lambda c=current_chat: self.open_chat(c)# Фиксируем значение
            ).grid(row=chat_id + 1, column=0,sticky="we", ipadx=6)

            Button(
                self.side,
                text="X",
                height=1,
                width=2,
                command=lambda c=current_chat: self.delete_chat(c)  # Фиксируем значение
            ).grid(row=chat_id + 1, column=1, ipadx=6)

            Button(
                self.side,
                text="✍",
                command=lambda c=current_chat: self.rename_chat(c)  # Фиксируем значение
            ).grid(row=chat_id + 1, column=2, ipadx=6)


    def create_chat(self):
        new_chat_name = simpledialog.askstring("New char", "Enter the chat name:", parent=self.root)

        if not new_chat_name:
            return

        # Проверяем уникальность имени
        if new_chat_name in self.chats:
            messagebox.showerror("Error", "A chat with this name already exists!", parent=self.root)
            return
        else:
            metaGenerator.save(new_chat_name,"")
            self.side.destroy()
            self.side_panel()
            self.open_chat(new_chat_name)


    def rename_chat(self, chat_label:str,new_chat_name= None):
        if new_chat_name is None:
            new_chat_name = simpledialog.askstring(f"Rename chat {chat_label}", "Enter the chat name:", parent=self.root)

        if not new_chat_name:
            return

        # Проверяем уникальность имени
        if new_chat_name in self.chats:
            messagebox.showerror("Error", "A chat with this name already exists!", parent=self.root)
            return
        else:
            os.rename(src=f"meta/chats/{chat_label}.txt", dst=f"meta/chats/{new_chat_name}.txt")
            self.chats[new_chat_name] = self.chats.pop(chat_label)
            self.side.destroy()
            self.side_panel()


    def delete_chat(self,chat_label:str):
        if askyesno("Confirmation", message=f"are you sure you want to delete '{chat_label}'?"):
            self.chats.pop(chat_label)
            os.remove(f"meta/chats/{chat_label}.txt")


            self.side.destroy()
            self.side_panel()
            self.open_chat(None)



        else:
            return


    def open_chat(self, chat_label:str):
        self.chosen_chat = chat_label

        self.panel.destroy()
        self.main_panel()
        self.panel.configure(text=chat_label)


    def main_panel(self):

        self.panel = LabelFrame(root, bg="#fafafa")
        self.panel.grid(row=0, column=1)

        self.chat_panel = tk.scrolledtext.ScrolledText(
            self.panel,
            state='disabled',
            wrap=tk.WORD,
            font=("Arial", 11),
            padx=15,
            pady=15,
            bg="#fafafa")
        self.chat_panel.grid(row=0,column=0,columnspan=2)

        self.chat_panel.tag_configure("user", foreground="#1565c0", justify="right")
        self.chat_panel.tag_configure("ai", foreground="#2e7d32", justify="left")
        self.chat_panel.tag_configure("system", foreground="#9e9e9e", justify="center", )
        self.chat_panel.tag_configure("thinking", foreground="#757575", font=("Arial", 10, "italic"))



        self.user_entry = Text(
            self.panel,
            height=3,
            state='normal' if self.chosen_chat is not None else "disable",
            wrap=tk.WORD,
            font=("Arial", 11),
            padx=5,
            pady=5,
            bg="#fafafa",
            borderwidth=0
            )
        self.user_entry.grid(row=1,column=0)

        self.send_btn = Button(self.panel,text="⬆",
                               state='normal' if self.chosen_chat is not None else "disable",
                               command=lambda : self.send_message(self.user_entry.get("1.0", "end"
                                                                                      ).strip()))
        self.send_btn.grid(row=1,column=1,ipadx=6, ipady=3)


        if self.chosen_chat is not None:
            for text in metaGenerator.load(self.chosen_chat):
                if text["role"] == "user":
                    self.chat_panel["state"] = "normal"
                    self.chat_panel.insert(END, f"\n{text["content"]}\n", "user")
                elif text["role"] == "assistant":
                    self.chat_panel.insert(END, f"\n{text["content"]}\n", "ai")







    def send_message(self,text):
        self.send_btn["state"] = "disable"
        self.user_entry.delete("1.0", END)

        self.chat_panel["state"] = "normal"

        self.chat_panel.insert(END, f"\n{text}\n", "user")

        ans = self.chats[self.chosen_chat].text_query(f"{text}")
        self.chat_panel.delete(f"{len(self.chat_panel.get("1.0", tk.END).splitlines())}.0", END)

        self.chat_panel.insert(END, f"\n{ans}\n", "ai")


        self.chat_panel["state"] = "disable"
        self.send_btn["state"] = "normal"
        metaGenerator.save(self.chosen_chat, self.chats[self.chosen_chat].history)




if __name__ == "__main__":
    root = tk.Tk()
    app = AIchatAPP(root)
    root.mainloop()