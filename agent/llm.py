import os
from dotenv import load_dotenv
import google.genai as genai
from dataclasses import dataclass
import time
from prompts import SYSTEM_PROMPT

@dataclass
class LLMResponse:
    text: str | None              # model's text reply ("" if none)
    tool_calls: list[dict]        # function_call steps the model requested
    raw: object                   # the full interaction object
    history: list                 # updated conversation history

    def __repr__(self) -> str:
        return (
            f"LLMResponse(text={self.text!r}, "
            f"tool_calls={self.tool_calls}, "
            f"history_len={len(self.history)})"
        )



load_dotenv()

client = genai.Client()

MODEL_NAME = "gemini-3.1-flash-lite"



def _send(history: list, tools: list[dict] | None = None) -> LLMResponse:
    
    #prepare the arguments for the interaction
    
    arguments = {
        "model": MODEL_NAME,
        "input": history,
        "store": False,
        "system_instruction": SYSTEM_PROMPT 
    }
    
    if tools:
        arguments["tools"] = tools
    
    interaction = client.interactions.create(
        **arguments,
    )

    reply = interaction.output_text
        
    # Append the model-generated steps to the history (must be saved as-is)
    steps =  [s.model_dump() for s in (interaction.steps or [])]
    history.extend(steps)
        
    return LLMResponse(
        text=reply,
        tool_calls=[s for s in steps if s.get("type") == "function_call"],
        raw=interaction,
        history=history,
    )
    


def chat(history: list, user_input: str , tools: list[dict] | None = None) -> LLMResponse:
  
    # Append the new user input to the history
    history.append({
        "type": "user_input",
        "content": [{"type": "text", "text": user_input}]
    })

    return _send(history, tools=tools)
    





if __name__ == "__main__":
    history = []

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

    response = chat(
        history,
        "List the files in the input folder. You must call the list_files tool.",
        tools=[list_files_tool],
    )

    print("text:", repr(response.text))
    print("tool_calls:", response.tool_calls)
    print("history types:", [s.get("type") for s in response.history])
