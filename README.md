# Offline-AI-Chat
Simple chat with artificial intelligence, with the ability to create different chats




![alt text](<Без имени.png>)
1. chat button
2. delete chat
3. rename xhat
4. chat field
5. input field
6. send button


---

A desktop chat interface for interacting with DeepSeek AI models, featuring persistent chat history management and a clean GUI.

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
- `metaGenerator.py` module

## Installation

1. You need intalled `Ollama`, you can dowload it from https://ollama.com/

2. you need to download right version of AI from https://ollama.com/search (I use deepseek-r1)

    The site presents different versions of the neural network and the command to launch it.

    **The larger the version size you choose, the "smarter" the chat will be.**
    1. Select the required version 
    2. Copy its name (deepseek-r1:latest)
    3. Run code `ollama run <your version>` to test (ollama run deepseek-r1:latest)
    4. Wait until the download is complete

    At this point you alredy have access to Ai, but only in console
    ![alt text](<Без имени-1.png>)

    
3. Select the desired version in main.py
    1. Open `main.py`
    2. serch for `AI.AI_chat`
    3. change the first parameter to your version (it should be downloaded)
4. Run `main.py`



### Interface Overview
- **Left Sidebar**: Shows all chat sessions
  - `+ new chat`: Create new chat session
  - `Chat Name`: Open existing chat (truncated to 10 chars)
  - `X`: Delete chat
  - `✍`: Rename chat
- **Main Panel**: Displays conversation history
  - User messages: Blue text, right-aligned
  - AI responses: Green text, left-aligned
- **Input Area**: Bottom text box for typing messages

### How to Use
1. Create a new chat using the `+ new chat` button
2. Type your message in the bottom text box
3. Press `⬆` or Enter to send
4. Switch between chats using the sidebar
5. Manage chats using rename/delete buttons

## File Structure
```
deepseek-chat/
├── meta/                # Chat storage
│   └── chats/           # Individual chat histories
├── AI.py                # DeepSeek integration
├── metaGenerator.py     # Chat history management
├── app.py               # Main application
└── README.md
```

## Customization
- Adjust window size in `__init__`:
```python
self.root.minsize(800, 500)
self.root.maxsize(1000, 700)
```
- Modify color schemes in `main_panel`:
```python
self.chat_panel.tag_configure("user", foreground="#1565c0")
self.chat_panel.tag_configure("ai", foreground="#2e7d32")
```
- Change AI model in `side_panel`:
```python
AI.AI_chat("deepseek-r1:latest", ...)
```
---