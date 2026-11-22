import os
from dotenv import load_dotenv
import google.genai as genai
import time

load_dotenv()

client = genai.Client()

MODEL_NAME = "gemini-3.1-flash-lite"

def chat(history: list, user_input: str) -> tuple[str, list]:
  
    # 1. Append the new user input to the history
    history.append({
        "type": "user_input",
        "content": [{"type": "text", "text": user_input}]
    })

    # 2. Send the request, key point: store=False
    interaction = client.interactions.create(
        model=MODEL_NAME,
        store=False,          # Disable server-side storage, manage state manually
        input=history
    )

    # 3. Get the reply
    reply = interaction.output_text

    # 4. Append the model-generated steps to the history (must be saved as-is)
    for step in interaction.steps:
        history.append(step.model_dump())

    return reply, history





if __name__ == "__main__":
    history = []

    reply, history = chat(history, "My name is Sahbi.")
    print("bot:", reply)

    reply, history = chat(history, "What is my name?")
    print("bot:", reply)

    reply, history = chat(history, "What did I ask you first?")
    print("bot:", reply)

    print("\n====================================================\n")
    print("History:")
    for step in history:
        print(step)
        