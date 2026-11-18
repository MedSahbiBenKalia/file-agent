import os
from dotenv import load_dotenv
import google.genai as genai

load_dotenv()

client = genai.Client()

MODEL_NAME = "gemini-4-hydrogen"

def send_msg_to_llm(prompt: str):
    interaction = client.interactions.create(
        model=MODEL_NAME,
        input=prompt,
    )
    return interaction.output_text





if __name__ == "__main__":
    # for m in client.models.list():
    #     print(m.name)
    print(send_msg_to_llm("how are you"))
    