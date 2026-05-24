import requests
from openai import OpenAI

client = OpenAI(api_key="AIzaSyA2T3ZZOuW503XCLlZJoAZTTyqtNppLIX0")  


class AIAgent:

    # 🌐 пошук в інтернеті
    def search_web(self, query: str):
        url = "https://api.duckduckgo.com/"
        params = {
            "q": query,
            "format": "json",
            "no_html": 1,
            "skip_disambig": 1
        }

        try:
            data = requests.get(url, params=params, timeout=5).json()
            return data.get("AbstractText") or "Інтернет не дав відповіді"
        except:
            return "Помилка інтернет-запиту"

    # ✏️ підрахунок букв
    def count_letters(self, text: str):
        return len([c for c in text if c.isalpha()])

    # 🤖 AI відповідь
    def ask_ai(self, question: str, web_info: str):
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "Ти корисний AI-агент, який використовує інформацію з інтернету."
                },
                {
                    "role": "user",
                    "content": f"Питання: {question}\n\nІнтернет: {web_info}"
                }
            ]
        )
        return response.choices[0].message.content

    # 🤖 головна функція агента
    def run(self, text: str):
        web_info = self.search_web(text)
        ai_answer = self.ask_ai(text, web_info)
        letters = self.count_letters(text)

        return (
            f"🌐 Інтернет дані:\n{web_info}\n\n"
            f"🤖 AI відповідь:\n{ai_answer}\n\n"
            f"✏️ Кількість букв: {letters}"
        )


agent = AIAgent()

while True:
    text = input("Питання: ")
    print(agent.run(text))