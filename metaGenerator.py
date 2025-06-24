
def save(chat_label, history):
    file  = open(f"meta/chats/{chat_label}.txt", "w+", encoding="UTF-8")
    for mess in history:
        file.write(f"{mess}\n")
    file.close()


def load(chat_label):
    file  = open(f"meta/chats/{chat_label}.txt", "r+", encoding="UTF-8")
    history = []

    for line in file:
        history.append(eval(line))
    file.close()

    return history

if __name__ == "__main__":
    save("test",[1,2,3,4,5,6,7,8,9,10])
    print(load("test"))