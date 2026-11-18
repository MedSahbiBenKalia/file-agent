from pathlib import Path


sandbox_dir = Path(__file__).resolve().parent.parent / "sandbox" 

def list_files(dir : str =".") ->list[str] :
    base = sandbox_dir / dir
    results = []
    for file in base.rglob("*"):
        if file.is_file():
            results.append(str(file.relative_to(sandbox_dir)).replace("\\", "/"))
    return results


def read_file(relative_path : str ) -> str :
    file_path = sandbox_dir / relative_path
    result =f"file_path: {relative_path}"
    file_content = ""
    if not file_path.exists():
        raise FileNotFoundError("file does not exists "+ relative_path)
    if not file_path.is_file():
        raise IsADirectoryError("this is a directory "+ relative_path)
    with open(file_path, "r", encoding="utf-8") as f:
        file_content = f.read()
    result += f"\nfile_content:\n{file_content}\n"
    return result

def write_file(relative_path : str = ".", content : str = "") -> str :
    file_path = sandbox_dir / relative_path
    file_path.parent.mkdir(parents=True, exist_ok=True)
    file_path.write_text(content, encoding="utf-8")
    return f"Wrote {len(content)} chars to {relative_path}"

def finish(summary: str) -> str:
    """Signal that the task is complete. The loop stops when this is called."""
    return f"DONE: {summary}"


TOOLS = [
    {
        "name": "list_files",
        "description": (
            "List all files inside a sandbox subdirectory, recursively. "
            "Use this FIRST to discover what input files are available "
            "before reading anything."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "dir": {
                    "type": "string",
                    "description": "Subdirectory relative to sandbox/, e.g. 'input' or '.'. Defaults to '.'.",
                }
            },
            "required": [],
        },
    },
    {
        "name": "read_file",
        "description": (
            "Read the full text contents of a file in the sandbox. "
            "Use this to read the profile, the resume template, or the job description."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "relative_path": {
                    "type": "string",
                    "description": "Path relative to sandbox/, e.g. 'input/profile.txt'.",
                }
            },
            "required": ["relative_path"],
        },
    },
    {
        "name": "write_file",
        "description": (
            "Write text to a file in the sandbox. Creates parent folders automatically "
            "and overwrites existing files. Use this to save the generated resume."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "relative_path": {
                    "type": "string",
                    "description": "Path relative to sandbox/, e.g. 'output/resume.md'.",
                },
                "content": {
                    "type": "string",
                    "description": "The full text content to write to the file.",
                },
            },
            "required": ["relative_path", "content"],
        },
    },
    {
        "name": "finish",
        "description": (
            "Call this when the task is fully complete. Provide a short summary "
            "of what was done. This stops the agent loop."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "summary": {
                    "type": "string",
                    "description": "Short summary of the completed task.",
                }
            },
            "required": ["summary"],
        },
    },
]


def dispatch(name: str, args: dict) -> str:
    if name == "list_files":
        return str(list_files(args.get("dir", ".")))
    if name == "read_file":
        return read_file(args["relative_path"])
    if name == "write_file":
        return write_file(args["relative_path"], args["content"])
    if name == "finish":
        return finish(args["summary"])
    return f"ERROR: unknown tool '{name}'"


if __name__ == "__main__":
    print("--- list_files ---")
    print(list_files())

    print("\n--- read_file ---")
    print(read_file("input/profile.txt"))

    print("\n--- write_file ---")
    print(write_file("output/test.txt", "this is a test"))

    print("\n--- dispatch: read_file ---")
    print(dispatch("read_file", {"relative_path": "input/profile.txt"}))

    print("\n--- finish ---")
    print(finish("everything works"))