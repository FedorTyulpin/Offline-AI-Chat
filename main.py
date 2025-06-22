import os
import threading
import tkinter as tk
from pkgutil import walk_packages
from selectors import SelectSelector
from tkinter import *
from tkinter import ttk
from tkinter import scrolledtext, messagebox, simpledialog
from tkinter.messagebox import askyesno



import AI
import metaGenerator


class AIchatAPP:

    def __init__(self, root:tk.Tk):

        self.chats = {}
        self.chosen_chat = None

        self.streaming_active = False
        self.current_stream_content = ""

        self.chat_panel = tk.scrolledtext.ScrolledText()
        self.root = root
        self.root.title("DeepSeek Chat")
        self.root.resizable(False, False)
        self.root.iconphoto(False, PhotoImage(file="meta/logo.png"))
        self.is_thinking  = IntVar()
        self.thinking_text = False
        self.bold_text_id = None
        self.italic_text_id = None

        self.main_panel()
        self.side_panel()

    def side_panel(self):

        self.side = LabelFrame(self.root,text="Chats",background="#212327",fg="#FFFAFA",borderwidth=0)
        self.side.grid(row=0, column=0,ipadx=5, ipady=5,sticky="nsew")

        new_chat_btn = Button(self.side,
                              text="+ new chat",
                              width=15,
                              background="#4D6BFE",
                              fg="#F8FAFC",
                              command=lambda : self.create_chat())
        new_chat_btn.grid(columnspan=3,sticky="n",padx=5,pady=5)

        chats_list = [i[:-4] for i in os.listdir("meta/chats")]

        for chat_id in range(len(chats_list)):
            current_chat = chats_list[chat_id]

            self.chats[current_chat] = AI.AI_chat(current_chat, history= metaGenerator.load(current_chat))

            Button(
                self.side,
                text=current_chat if len(current_chat) <= 10 else current_chat[:7]+"...",
                borderwidth=0,
                bg="#212327",
                fg="#CFD0D3",
                cursor="hand2",
                state="normal" if current_chat != self.chosen_chat else "disable",
                command=lambda c=current_chat: self.open_chat(c)
            ).grid(row=chat_id + 1, column=0,sticky="we", padx=6)

            Button(
                self.side,
                text="X",
                height=1,
                width=2,
                borderwidth=0,
                bg="#212327",
                fg="#CFD0D3",
                cursor="hand2",
                command=lambda c=current_chat: self.delete_chat(c)
            ).grid(row=chat_id + 1, column=1, ipadx=3)

            Button(
                self.side,
                text="✍",
                borderwidth=0,
                bg="#212327",
                fg="#CFD0D3",
                cursor="hand2",
                command=lambda c=current_chat: self.rename_chat(c)
            ).grid(row=chat_id + 1, column=2, ipadx=3)


    def create_chat(self):
        new_chat_name = simpledialog.askstring("New chat", "Enter the chat name:", parent=self.root)

        if not new_chat_name:
            return

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
        self.side.destroy()
        self.main_panel()
        self.side_panel()
        self.panel.configure(text=chat_label)


    def main_panel(self):

        self.panel = LabelFrame(root, background="#292A2D",fg="#FFFFFF",labelanchor="n",borderwidth=0,font=("Arial", 11))
        self.panel.grid(row=0, column=1)

        self.chat_panel = tk.scrolledtext.ScrolledText(
            self.panel,
            state='disabled',
            wrap=tk.WORD,
            font=("Arial", 11),
            padx=15,
            pady=15,
            bg="#292A2D",
            fg="#FFFFFF",
            borderwidth=0)
        self.chat_panel.grid(row=0,column=0,columnspan=2)

        self.chat_panel.tag_configure("user", foreground="#F8FAFF", justify="right",font=("Arial", 10))
        self.chat_panel.tag_configure("ai", foreground="#F8FAFF", justify="left",font=("Arial", 10))
        self.chat_panel.tag_configure("system", foreground="#9e9e9e", justify="center")
        self.chat_panel.tag_configure("thinking", foreground="#757575", font=("Arial", 10, "italic"))


        self.chat_panel.tag_configure("bold", foreground="#979AAA", font=("Arial", 10, "bold"))
        self.chat_panel.tag_configure("italic", foreground="#F8FAFF", font=("Arial", 10, "italic"))
        self.chat_panel.tag_configure("underline", underline=True, font=("Arial", 10))
        self.chat_panel.tag_configure("strike", overstrike=True, font=("Arial", 10))


        self.chat_panel.tag_configure("H1", overstrike=True, font=("Arial", 15, "bold"))
        self.chat_panel.tag_configure("H2", overstrike=True, font=("Arial", 12, "bold"))
        self.chat_panel.tag_configure("H3", overstrike=True, font=("Arial", 11, "bold"))



        self.is_thinking_flag = ttk.Checkbutton(self.panel,
                                                text="deep think",
                                                state="disable" if self.chosen_chat is None else "normal",
                                                variable=self.is_thinking)
        self.is_thinking_flag.grid(row=1,column=0, sticky="w")



        self.user_entry = Text(
            self.panel,
            height=3,
            state='normal' if self.chosen_chat is not None else "disable",
            wrap=tk.WORD,
            font=("Arial", 11),
            padx=5,
            pady=5,

            background="#404045",
            fg="#FFFFFF",
            borderwidth=0
            )
        self.user_entry.grid(row=2,column=0, ipadx=5, ipady=5, padx=5,pady=5)



        self.send_btn = Button(self.panel,
                               text="⬆",
                               background="#4D6BFE",
                               fg="#F7F9FF",
                               padx=6,
                               pady=3,
                               height=1,
                               width=1,
                               state='normal' if self.chosen_chat is not None else "disable",
                               command=lambda : self.send_message(self.user_entry.get("1.0", "end"
                                                                                      ).strip()))
        self.send_btn.grid(row=2,column=1,ipadx=3, ipady=3)


        if self.chosen_chat is not None:
            for text in metaGenerator.load(self.chosen_chat):
                if text["role"] == "user":
                    self.chat_panel["state"] = "normal"
                    self.chat_panel.insert(END, f"\n\n{text["content"]}\n\n", "user")
                elif text["role"] == "assistant":

                    for word in text["content"].replace("<think>", " <think> ").replace("</think>", " </think> ").replace("**", " ** ").replace("__", " __ ").split(" "):
                        if word == "<think>":
                            self.thinking_text = True
                            self.chat_panel.insert(END, f"-------------------------------------",
                                                   "thinking")
                        elif word == "</think>":
                            self.thinking_text = False
                            self.chat_panel.insert(END, f"-------------------------------------",
                                                   "thinking")

                        elif (word == "**" or word=="__") and not self.thinking_text:
                            if self.bold_text_id is None:
                                self.bold_text_id = self.chat_panel.index("end-1c")
                            else:
                                self.chat_panel.tag_add("bold", self.bold_text_id, self.chat_panel.index("end-1c"))
                                self.bold_text_id = None

                        elif (word.startswith("*") and word.endswith("*")) and not self.thinking_text:
                            if self.italic_text_id is None:
                                self.italic_text_id = self.chat_panel.index("end-1c")
                            else:
                                self.chat_panel.tag_add("italic", self.italic_text_id, self.chat_panel.index("end-1c"))
                                self.italic_text_id = None

                        else:
                            self.chat_panel.insert(END, f"{word} ", "thinking" if self.thinking_text else "ai")

    def send_message(self, text):
        if self.streaming_active:
            return

        self.streaming_active = True
        self.send_btn["state"] = "disabled"
        self.user_entry.delete("1.0", END)
        self.user_entry["state"] = "disabled"


        self.chat_panel["state"] = "normal"
        self.chat_panel.insert(END, f"\n{text}\n", "user")


        thinking_line = self.chat_panel.index(END)

        self.chat_panel.insert(END, "\nThinking...\n", "thinking")
        self.chat_panel.see(END)
        self.chat_panel.update()


        self.current_stream_content = ""


        thread = threading.Thread(
            target=self.start_stream_query,
            args=(text, thinking_line),
            daemon=True
        )
        thread.start()

    def start_stream_query(self, text, thinking_line):
        """Запускает потоковый запрос"""
        try:

            self.chats[self.chosen_chat].stream_query(
                text,
                lambda chunk: self.root.after(0, self.update_stream, chunk, thinking_line),
                is_thinking=self.is_thinking.get())
        except Exception as e:
            error_msg = f"⚠️ Error: {str(e)}"
            self.root.after(0, self.finalize_stream, error_msg, True, thinking_line)
        finally:
            self.root.after(0, self.finalize_stream, "", False, thinking_line)

    def update_stream(self, chunk, thinking_line):
        """Обновляет интерфейс новой частью ответа"""
        if not self.streaming_active:
            return

        self.chat_panel["state"] = "normal"



        if chunk == "<think>":
            self.thinking_text = True
            self.chat_panel.insert(END, f"\n-------------------------------------",
                                   "thinking")
        elif chunk == '</think>':
            self.thinking_text = False
            self.chat_panel.insert(END, f"-------------------------------------",
                                   "thinking")
        elif ("**" in chunk or "__" in chunk) and not self.thinking_text:
            self.chat_panel.insert(END, chunk.replace("_","*").split("**")[0], "ai")

            if self.bold_text_id is None:
                self.bold_text_id = self.chat_panel.index("end-1c")
            else:
                self.chat_panel.tag_add("bold", self.bold_text_id, self.chat_panel.index("end-1c"))
                self.bold_text_id = None

        elif ("*" in chunk or "_" in chunk) and not self.thinking_text:
            self.chat_panel.insert(END, chunk.replace("_","*").split("*")[0], "ai")

            if self.bold_text_id is None:
                self.bold_text_id = self.chat_panel.index("end-1c")
            else:
                self.chat_panel.tag_add("italic", self.bold_text_id, self.chat_panel.index("end-1c"))
                self.bold_text_id = None



        else:
            if not self.current_stream_content:
                self.chat_panel.delete(thinking_line, f"{thinking_line}+2l")

                self.ai_response_start = self.chat_panel.index(END)
                self.chat_panel.insert(END, chunk, "thinking" if self.thinking_text else "ai")
            else:

                self.chat_panel.insert(END, chunk, "thinking" if self.thinking_text else "ai")


            self.current_stream_content += chunk
            self.chat_panel.see(END)
            self.chat_panel["state"] = "disabled"

    def finalize_stream(self, error_msg, is_error, thinking_line):
        """Завершает потоковый вывод"""
        self.chat_panel["state"] = "normal"

        if is_error:

            if not self.current_stream_content:
                self.chat_panel.delete(thinking_line, f"{thinking_line}+2l")
                self.chat_panel.insert(END, f"\n{error_msg}\n", "system")
            else:
                self.chat_panel.insert(END, f"\n{error_msg}\n", "system")
        elif self.current_stream_content:

            self.chat_panel.insert(END, "\n", "ai")

        self.chat_panel["state"] = "disabled"
        self.bold_text = False


        if not is_error and self.current_stream_content:
            metaGenerator.save(self.chosen_chat, self.chats[self.chosen_chat].history)


        self.user_entry["state"] = "normal"
        self.send_btn["state"] = "normal"
        self.streaming_active = False
        self.current_stream_content = ""


if __name__ == "__main__":
    root = tk.Tk()
    app = AIchatAPP(root)
    root.mainloop()