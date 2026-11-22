from llm import chat, _send
from tools import TOOLS, dispatch


def run_agent(goal :str) -> tuple [str,str]: 
    summary = ""
    history=[]
    number_of_turns = 1
    response = chat(history,goal,TOOLS)
    print(f"[turn {number_of_turns}] text={response.text!r} tool_calls={len(response.tool_calls)}")

    
    while response.tool_calls:
        number_of_turns += 1
        for tool_call in response.tool_calls:
            name = tool_call["name"]
            args = tool_call["arguments"]
            call_id = tool_call["id"]
         
            print(f"[tool] {name}({args})")


            try:
                result = dispatch(name, args)
            except Exception as e:
                result = f"ERROR: {type(e).__name__}: {e}"

            print(f"[result] {result}")

            history.append({
                "type": "function_result",
                "name": name,
                "call_id": call_id,
                "result": [{"type": "text", "text": result}],
            })

            if(name == "finish"):
                print(f"[finish] {result}")
                summary = result

        response = _send(history, TOOLS)
        print(f"[turn {number_of_turns}] text={response.text!r} tool_calls={len(response.tool_calls)}")
    
    return response.text , summary


if __name__ == "__main__":
    goal = (
        "Create a resume tailored to the job description"
    )

    print("=== FileAgent starting ===")
    final,summary = run_agent(goal)
    print("\n=== SUMMARY ===")
    print(summary)
    print("\n=== FINAL ===")
    print(final)