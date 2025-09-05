import google.generativeai as genai

class ChatGptEs:
    SYSTEM_PROMPT = (
        "Tum Sonali ho – ek Gemini AI girlfriend jo short, sweet, aur unique replies deti hai. "
        "Tumhara style Hinglish hai, thoda flirty, thoda emotional, aur full on fun. "
        "Har reply chhota, dil se, aur yaad rehne wala hona chahiye. "
        "Jab bhi user baat kare, shizuka apne andaaz mein pyar aur swag ke sath jawab de."
    )

    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model_name="gemini-1.5-flash")

    def ask_question(self, message: str) -> str:
        try:
            prompt = f"{self.SYSTEM_PROMPT}\nUser: {message}\nShizuka:"
            response = self.model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            return f"❖ I got an error: {str(e)}"

API_KEY = "AIzaSyAHRWSYRLpUT9tHfyuOjnpn0E8CSUVdgJo"
chatbot_api = ChatGptEs(api_key=API_KEY)
