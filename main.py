import os
import threading
import tkinter as tk
from pkgutil import walk_packages
from selectors import SelectSelector
from tkinter import *
from tkinter import ttk
from tkinter import scrolledtext, messagebox, simpledialog
from tkinter.messagebox import askyesno



from AI import AI_chat
import metaGenerator


class AIchatAPP:
    """
    The main class of the application, here you can find everything related to the interface and its functionality

    :param root: the main root element of the window
    """
    def __init__(self, root:tk.Tk) -> None:

        self.chats: dict[str : AI_chat] = {}
        self.chosen_chat: str | None = None

        self.streaming_active: bool = False
        self.current_stream_content: str = ""

        self.chat_panel = tk.scrolledtext.ScrolledText()
        self.root: tk.Tk = root
        self.root.title("DeepSeek Chat")
        self.root.resizable(False, False)
        self.root.iconphoto(False, PhotoImage(file="meta/logo.png"))
        self.is_thinking = IntVar()
        self.thinking_text: bool = False
        self.bold_text_id: str | None = None
        self.italic_text_id: str | None = None
        self.quote_text_id: str | None = None

        self.header_text: tuple[str, int] | None = None

        self.code_text_id: str | None = None
        self.first_line_of_code: bool = False


        self.main_panel()
        self.side_panel()

    def side_panel(self) -> None:
        """
        Function generating sidebar with chats
        """

        self.side: tk.LabelFrame = LabelFrame(self.root,text="Chats",background="#212327",fg="#FFFAFA",borderwidth=0) #tk
        self.side.grid(row=0, column=0,ipadx=5, ipady=5,sticky="nsew")

        new_chat_btn = Button(self.side,
                              text="+ new chat",
                              width=15,
                              background="#4D6BFE",
                              fg="#F8FAFC",
                              command=lambda : self.create_chat())
        new_chat_btn.grid(columnspan=3,sticky="n",padx=5,pady=5)

        chats_list: list[str] = [i[:-4] for i in os.listdir("meta/chats")]

        for chat_id in range(len(chats_list)):
            current_chat: str = chats_list[chat_id]

            self.chats[current_chat] = AI_chat(current_chat, history= metaGenerator.load(current_chat))

            # rendering the fucking buttons
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
            # stop rendering the fucking buttons


    def create_chat(self) -> None:
        """Creating a chat with selecting a name for it"""
        new_chat_name: str | None = simpledialog.askstring("New chat", "Enter the chat name:", parent=self.root)

        if not new_chat_name:
            return # It's not a mistake. There's nothing here.

        if new_chat_name in self.chats:
            messagebox.showerror("Error", "A chat with this name already exists!", parent=self.root)
            return # and here, too...
        else:
            metaGenerator.save(new_chat_name,"")
            self.side.destroy()
            self.side_panel()
            self.open_chat(new_chat_name)


    def rename_chat(self, chat_label: str ,new_chat_name: str | None = None) -> None:
        """Renaming a chat"""
        if new_chat_name is None:
            new_chat_name = simpledialog.askstring(f"Rename chat {chat_label}", "Enter the chat name:", parent=self.root)

        if not new_chat_name:
            return # again.

        if new_chat_name in self.chats:
            messagebox.showerror("Error", "A chat with this name already exists!", parent=self.root)
            return # ...
        else:
            os.rename(src=f"meta/chats/{chat_label}.txt", dst=f"meta/chats/{new_chat_name}.txt")
            self.chats[new_chat_name] = self.chats.pop(chat_label)
            self.side.destroy() #tk
            self.side_panel() 


    def delete_chat(self,chat_label:str) -> None :
        if askyesno("Confirmation", message=f"Are you sure you want to delete '{chat_label}'?"): #tk
            self.chats.pop(chat_label)
            os.remove(f"meta/chats/{chat_label}.txt")


            self.side.destroy() #tk
            self.side_panel()
            self.open_chat(None)



        else:
            return # :)


    def open_chat(self, chat_label: str) -> None:
        """Opening a chat"""
        self.chosen_chat: str = chat_label

        self.panel.destroy() #tk
        self.side.destroy() #tk
        self.main_panel()
        self.side_panel()
        self.panel.configure(text=chat_label) #tk
        self.chat_panel.see(END) #tk


    def main_panel(self) -> None:
        """Generating main panel of the window"""


        # tk start
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

        self.chat_panel.bind("<Control-c>", lambda e: self.chat_panel.event_generate("<<Copy>>"))


        self.chat_panel.grid(row=0,column=0,columnspan=2)


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

        self.user_entry.bind("<Control-c>", lambda e: self.user_entry.event_generate("<<Copy>>"))
        self.user_entry.bind("<Command-v>", lambda e: self.user_entry.event_generate("<<Paste>>"))
        self.user_entry.bind("<Control-x>", lambda e: self.user_entry.event_generate("<<Cut>>"))

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

        self.chat_panel.tag_configure("user", foreground="#F8FAFF", justify="right", font=("Arial", 10))
        self.chat_panel.tag_configure("ai", foreground="#F8FAFF", justify="left", font=("Arial", 10))
        self.chat_panel.tag_configure("system", foreground="#9e9e9e", justify="center")
        self.chat_panel.tag_configure("thinking", foreground="#757575", font=("Arial", 10, "italic"))

        self.chat_panel.tag_configure("bold", foreground="#979AAA", font=("Arial", 10, "bold"))
        self.chat_panel.tag_configure("italic", foreground="#F8FAFF", font=("Arial", 10, "italic"))
        self.chat_panel.tag_configure("underline", underline=True, font=("Arial", 10))
        self.chat_panel.tag_configure("strike", overstrike=True, font=("Arial", 10))

        self.chat_panel.tag_configure("code", background="#212327", font=("Courier", 10), borderwidth=0, relief="solid")
        self.chat_panel.tag_configure("codetitle", background="#404045", font=("Courier", 10), borderwidth=0, relief="solid")
        self.chat_panel.tag_configure("quote", foreground="#F8FAF3",background="#424242",font=("Arial", 10, "bold"))
        self.chat_panel.tag_configure("link", foreground="blue", underline=True)


        self.chat_panel.tag_configure("H1",foreground="#F8FAFF", font=("Arial", 15, "bold"))
        self.chat_panel.tag_configure("H2",foreground="#F8FAFF", font=("Arial", 14, "bold"))
        self.chat_panel.tag_configure("H3",foreground="#F8FAFF", font=("Arial", 12, "bold"))

        #tk end

        if self.chosen_chat is not None:
            for text in metaGenerator.load(self.chosen_chat): #history of selected chat
                if text["role"] == "user":
                    self.chat_panel["state"] = "normal" #tk
                    self.chat_panel.insert(END, f"\n\n{text["content"]}\n\n", "user") #tk
                elif text["role"] == "assistant":

                    # There's no God
                    text["content"] = text["content"].replace("```", "©")

                    for rep in ["<think>","</think>","**","__", "`","©"]:
                        text["content"] = text["content"].replace(rep, f" {rep} ")


                    for word in text["content"].split(" "):


                        if word == "<think>":
                            self.thinking_text: bool = True
                            self.chat_panel.insert(END, f"-------------------------------------",
                                                   "thinking")
                        elif word == "</think>":
                            self.thinking_text = False
                            self.chat_panel.insert(END, f"-------------------------------------",
                                                   "thinking")


                        elif "\n" in word and self.header_text is not None:
                            self.chat_panel.tag_add(f"H{self.header_text[1]}", self.header_text[0], self.chat_panel.index("end-1c"))
                            self.chat_panel.insert(END, f"\n{word} ", "ai")
                            self.header_text = None

                        elif word == "©" and not self.thinking_text:
                            if self.code_text_id is None:
                                self.first_line_of_code = True
                            else:
                                self.chat_panel.tag_add("code",str(float(self.code_text_id)-0.1), str(float(self.chat_panel.index("end"))-1))
                                self.code_text_id = None

                        elif self.first_line_of_code:
                            self.chat_panel.insert(END, f"{word} ")
                            self.chat_panel.tag_add("codetitle",
                                                    str(float(self.chat_panel.index("end"))-2), str(float(self.chat_panel.index("end"))-1))
                            self.code_text_id = self.chat_panel.index("end-1c")
                            self.first_line_of_code = False

                        elif word=="`" and (not self.thinking_text or self.code_text_id is not None ):
                            if self.quote_text_id is None:
                                self.quote_text_id = self.chat_panel.index("end-1c")
                            else:
                                self.chat_panel.tag_add("quote", self.quote_text_id, self.chat_panel.index("end-2c"))
                                self.quote_text_id = None

                        elif self.quote_text_id is None and self.code_text_id is None:

                            if "#" in word and not self.thinking_text:
                                if "###" in word:
                                    word = "".join(word.split("#"))
                                    self.chat_panel.insert(END, f"{word} \n", "ai")
                                    self.header_text = (self.chat_panel.index("end-1c"), 1)

                                elif "##" in word:
                                    word = "".join(word.split("##"))
                                    self.chat_panel.insert(END, f"{word} \n", "ai")
                                    self.header_text = (self.chat_panel.index("end-1c"), 2)

                                else:
                                    word = "".join(word.split("###"))
                                    self.chat_panel.insert(END, f"{word} \n", "ai")
                                    self.header_text = (self.chat_panel.index("end-1c"), 3)

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
                        else:
                            self.chat_panel.insert(END, f"{word} ", "thinking" if self.thinking_text else "ai")

            self.chat_panel["state"] = "disable"

    def send_message(self, text: str) -> None:
        """Sends a message and starts a streaming request"""
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

    def start_stream_query(self, text: str, thinking_line) -> None:
        """Runs a streaming request"""
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

    def update_stream(self, chunk: str, thinking_line) -> None:
        """Updates the interface with a new response part"""
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

    def finalize_stream(self, error_msg: str, is_error: bool, thinking_line) -> None:
        """Ends streaming output"""
        self.chat_panel["state"] = "normal"

        if is_error:

            if not self.current_stream_content:
                self.chat_panel.delete(thinking_line, f"{thinking_line}+2l")
                self.chat_panel.insert(END, f"\n{error_msg}\n", "system")
            else:
                self.chat_panel.insert(END, f"\n{error_msg}\n", "system")
        elif self.current_stream_content:

            self.chat_panel.insert(END, "\n", "ai")

        if not is_error and self.current_stream_content:
            metaGenerator.save(self.chosen_chat, self.chats[self.chosen_chat].history)

        self.chat_panel["state"] = "disabled"
        self.user_entry["state"] = "normal"
        self.send_btn["state"] = "normal"
        self.streaming_active = False
        self.current_stream_content = ""


        self.panel.destroy()
        self.main_panel()


if __name__ == "__main__":
    root = tk.Tk()
    app = AIchatAPP(root)
    root.mainloop()