class LetterAgent:
    def run(self, text: str):
        letters = [ch for ch in text if ch.isalpha()]
        return len(letters)


agent = LetterAgent()

while True:
    text = input("Введіть текст: ")
    print("Кількість букв:", agent.run(text))
    