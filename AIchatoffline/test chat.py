import AI
import metaGenerator

chat1 = AI.AI_chat('deepseek-r1:latest',"test")

def main():
    print("Ollama Chat (для выхода введите '0')")

    imp = input("Вы: ")
    while imp != "0":
        ret = chat1.text_query(imp, is_thinking=True)
        print(ret)

        imp = input("Вы: ")




if __name__ == "__main__":
    main()
    print(chat1.history)
    metaGenerator.save("test", chat1.history)

    print(metaGenerator.load("test"))
