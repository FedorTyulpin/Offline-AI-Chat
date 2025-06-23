
# Offline-AI-Chat
Simple chat with artificial intelligence, with the ability to create different chats
A desktop chat interface for interacting with DeepSeek AI models, featuring persistent chat history management and a clean GUI.

Смотрите [документацию](./README_ru.md) на русском

### Interface
1. create chat
2. rename chat (button)
3. delete chat (button)
4. select chat (button)
5. chat title
6. deep think button
7. input box
8. send Button

---



## Features

- 💬 Chat with DeepSeek-R1 AI model
- 📁 Multiple chat session management
- ➕ Create new chats
- ✏️ Rename existing chats
- ❌ Delete unwanted chats
- 💾 Automatic chat history saving
- 📜 Scrollable chat history
- 🖥️ Responsive UI with adjustable window size

## Requirements

- Python 3.8+
- Tkinter (usually included with Python)
- DeepSeek API access (through your `AI.py` module)
- Libraries from `requirements.txt` downloaded
- Installed `Ollama`

## Installation

1. You need intalled `Ollama`, you can dowload it from https://ollama.com/

2. you need to download right version of AI from https://ollama.com/search (I use deepseek-r1)

    The site presents different versions of the neural network and the command to launch it.

    **The larger the version size you choose, the "smarter" the chat will be.**
    1. Select the required version 
    2. Copy its name (deepseek-r1:latest)
    3. Run code `ollama run <your version>` to download model (ollama run deepseek-r1:latest)
    4. Wait until the download is complete

    At this point you alredy have access to Ai, but only in console
    
3. Run `main.py`



### Interface Overview
- **Left Sidebar**: Shows all chat sessions
  - `+ new chat`: Create new chat session
  - `Chat Name`: Open existing chat (truncated to 10 chars)
  - `X`: Delete chat
  - `✍`: Rename chat
- **Main Panel**: Displays conversation history
  - User messages: right-aligned
  - AI responses: left-aligned
  - If "deep think" on train of thought of the neural network will de grey
- **Input Area**: Bottom text box for typing messages

### How to Use
1. Create a new chat using the `+ new chat` button
2. Type your message in the bottom text box
3. Press `⬆` or Enter to send
4. Switch between chats using the sidebar
5. Manage chats using rename/delete buttons


---
