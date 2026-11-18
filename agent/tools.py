from pathlib import Path


sandbox_dir=Path("sandbox")

def list_files(dir : str =".") ->list[str] :
    base = sandbox_dir / dir
    results = []
    for file in base.rglob("*"):
        if file.is_file():
            results.append(str(file.relative_to(sandbox_dir)).replace("\\", "/"))
    return results


print(list_files())