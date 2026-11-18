from pathlib import Path


sandbox_dir=Path("sandbox")

def list_files(dir : str =".") ->list[str] :
    base = sandbox_dir / dir
    results = []
    for file in base.rglob("*"):
        if file.is_file():
            results.append(str(file.relative_to(sandbox_dir)).replace("\\", "/"))
    return results


def read_file(relative_path : str = ".") -> str :
    file_path = sandbox_dir / relative_path
    result =f"file_path: {relative_path}"
    file_content = ""
    if not file_path.exists():
        raise FileExistsError("file does not exists "+ relative_path)
    if not file_path.is_file():
        raise IsADirectoryError("this is a directory "+ relative_path)
    with open(file_path, "r", encoding="utf-8") as f:
        file_content = f.read()
    result += f"\nfile_content:\n{file_content}\n"
    return result





#print(list_files())
print(read_file("input/profile.txt"))