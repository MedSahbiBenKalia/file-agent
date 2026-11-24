from llm import chat, _send
from tools import TOOLS, dispatch
from logger import Logger


def run_agent(goal :str) -> tuple [str,str]: 

    logger = Logger()
    logger.log(f"=== goal ===")
    logger.log(goal)
    
    summary = ""
    history=[]
    number_of_turns = 1
    
    logger.log(f"=== FileAgent starting ===")
    response = chat(history,goal,TOOLS)
    logger.log(f"[turn {number_of_turns}] text={response.text!r} tool_calls={len(response.tool_calls)}")

    
    while response.tool_calls:
        number_of_turns += 1
        for tool_call in response.tool_calls:
            name = tool_call["name"]
            args = tool_call["arguments"]
            call_id = tool_call["id"]
         
            logger.log(f"[tool] {name}({args})")


            try:
                result = dispatch(name, args)
            except Exception as e:
                result = f"ERROR: {type(e).__name__}: {e}"

            logger.log(f"[result] {result}")

            history.append({
                "type": "function_result",
                "name": name,
                "call_id": call_id,
                "result": [{"type": "text", "text": result}],
            })

            if(name == "finish"):
                logger.log(f"[finish] {result}")
                summary = result

        response = _send(history, TOOLS)
        logger.log(f"[turn {number_of_turns}] text={response.text!r} tool_calls={len(response.tool_calls)}")
    
    logger.close()
    return response.text , summary


if __name__ == "__main__":
    goal = (
        "Create a resume tailored to the job description"
    )
    final,summary = run_agent(goal)
