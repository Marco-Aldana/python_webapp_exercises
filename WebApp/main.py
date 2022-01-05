import os
from project import app

if __name__ == "__main__":
    os.system("uvicorn main:app --reload")
