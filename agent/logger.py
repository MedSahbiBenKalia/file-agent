from pathlib import Path
from datetime import datetime

class Logger:
    def __init__(self, log_dir: str = "logs",name : str = "run"):
        logs_dir = Path(__file__).resolve().parent.parent / log_dir
        logs_dir.mkdir(exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.path = logs_dir / f"{name}_{timestamp}.log"
        self.file = open(self.path, "w", encoding="utf-8")

    def log(self, line: str = ""):
        print(line)
        self.file.write(line + "\n")
        self.file.flush()    # write immediately

    def close(self):
        self.file.close()



if __name__ == "__main__":
    logger = Logger(log_dir="test_logs", name="test")
    logger.log("This is a test log entry.")
    logger.log("Line 1")
    logger.log("Line 2")
    logger.close()