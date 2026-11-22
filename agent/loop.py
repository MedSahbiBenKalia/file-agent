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
        "You are a resume-writing agent working inside a sandbox folder. "
        "Do the following:\n"
        "1. Call list_files on 'input' to see what input files exist.\n"
        "2. Read sandbox/input/profile.txt and sandbox/templates/resume_template.md.\n"
        "3. Write a complete resume to sandbox/output/resume.md, "
        "filling the template with the profile's information. Do not invent facts.\n"
        "4. When the file is written, call the finish tool with a short summary."
    )

    print("=== FileAgent starting ===")
    final,summary = run_agent(goal)
    print("\n=== SUMMARY ===")
    print(summary)
    print("\n=== FINAL ===")
    print(final)