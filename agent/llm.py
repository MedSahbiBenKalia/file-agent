import os
from dotenv import load_dotenv
import google.genai as genai
import time

load_dotenv()

client = genai.Client()

MODEL_NAME = "gemini-3.1-flash-lite"

def chat(history: list, user_input: str , tools: list[dict] | None = None) -> tuple[str, list]:
  
    # Append the new user input to the history
    history.append({
        "type": "user_input",
        "content": [{"type": "text", "text": user_input}]
    })

    #prepare the arguments for the interaction

    arguments = {
        "model": MODEL_NAME,
        "input": history,
        "store": False, 
    }

    if tools:
        arguments["tools"] = tools



    interaction = client.interactions.create(
        **arguments,
    )

    # Get the reply
    reply = interaction.output_text

    # Append the model-generated steps to the history (must be saved as-is)
    for step in interaction.steps:
        history.append(step.model_dump())

    return reply, history





if __name__ == "__main__":
    history = []

    # test of history and chat function
    # reply, history = chat(history, "My name is Sahbi.")
    # print("bot:", reply)

    # reply, history = chat(history, "What is my name?")
    # print("bot:", reply)

    # reply, history = chat(history, "What did I ask you first?")
    # print("bot:", reply)

    # print("\n====================================================\n")
    # print("History:")
    # for step in history:
    #     print(step)




    # test of tools 
    list_files_tool = {
        "type": "function",
        "name": "list_files",
        "description": "List all files inside a sandbox subdirectory.",
        "parameters": {
            "type": "object",
            "properties": {
                "dir": {"type": "string", "description": "Subdirectory, e.g. 'input'."}
            },
            "required": [],
        },
    }

    reply, history = chat(
        history,
        "List the files in the input folder. You must call the list_files tool.",
        tools=[list_files_tool],
    )

    print("reply:", repr(reply))
    print("\n--- steps ---")
    for step in history:
        print(" type:", step.get("type"))
        if step.get("type") == "function_call":
            print("   name:", step.get("name"))
            print("   arguments:", step.get("arguments"))
