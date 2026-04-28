from openai import OpenAI

# 🔑 Use your Groq API key
client = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key="YOUR_API_KEY_HERE"
)

def chatbot_response(question, score):
    prompt = f"""
    You are a smart AI productivity coach.

    User score: {score}/10
    Question: {question}

    Give short, practical advice.
    """

    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",   # 🔥 Fast & free model
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"Error: {str(e)}"
