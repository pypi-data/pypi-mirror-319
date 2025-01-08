import subprocess
import typer
from pathlib import Path
import os



FOLDERS = ["base", "api", "models", "other", "schemas"]
INIT_FILE = "__init__.py"
FILES_INSIDE_MAIN = ["main.py", ".env", ".test.env", "pytest.ini"]

TEMPLATES = {
    "pytest.ini": """
[pytest]
pythonpath = .

env_files = 
    .test.env
""",
    ".env": """
DB_USER=postgres
DB_HOST=localhost
DB_PASSWORD=12345
DB_PORT=5432
DB_NAME=
SECRET_KEY=bingo
ACCESS_TOKEN_EXPIRE_MINUTES=60
ALGORITHM=HS256

MODE = 
""",
    "db.py": """
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from .config import settings

engine = create_engine(settings.connection_string, echo=True)

SessionLocal = sessionmaker(
    bind=engine,
    expire_on_commit=False,
)

def get_db():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()

class Base(DeclarativeBase):
    pass
""",
    "config.py": """
from pydantic_settings import BaseSettings
from pydantic import ConfigDict
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    DB_USER: str 
    DB_HOST: str 
    DB_PASSWORD: str 
    DB_PORT: str 
    DB_NAME: str 
    MODE: str

    SECRET_KEY: str 
    ACCESS_TOKEN_EXPIRE_MINUTES: int 
    ALGORITHM: str 

    @property
    def connection_string(self):
        return (
            f'postgresql+psycopg2://'
            f'{self.DB_USER}:'
            f'{self.DB_PASSWORD}@'
            f'{self.DB_HOST}:{self.DB_PORT}/'
            f'{self.DB_NAME}'
        )
        
    def connection_string(self):
        return (
    model_config = ConfigDict(env_file=".env")

settings = Settings()
""",
    "conftest.py": """
import pytest
from src.base.config import settings
from src.base.db import Base, engine, SessionLocal

@pytest.fixture(scope="session", autouse=True)
def setup_db():
    assert settings.MODE == "TEST"
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    
@pytest.fixture()
def db():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
""",
    "main.py": """
from fastapi import FastAPI
import uvicorn

app = FastAPI()

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True, host="0.0.0.0")
""",
}

def create_folder(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)

def create_file_with_content(path: Path, file_name: str, content: str = "") -> None:
    file_path = path / file_name
    file_path.write_text(content)

    # command_req = "pip install -r requirements.txt"
    # try:
    #         result = subprocess.run(command_req, shell=True, check=True, text=True, capture_output=True, cwd=os.getcwd())
    #         print("Pip install output:", result.stdout)
    # except subprocess.CalledProcessError as e:
    #         print("Pip install error:", e.stderr)

def setup_main_folder(main_path: Path):
    create_folder(main_path)

    for file_name in FILES_INSIDE_MAIN:
        content = TEMPLATES.get(file_name, "")
        create_file_with_content(main_path, file_name, content)


    env_content = TEMPLATES[".env"]
    create_file_with_content(main_path, ".env", env_content)
    create_file_with_content(main_path, ".test.env", env_content)
    

    command = "alembic init alembic"
    try:
        result = subprocess.run(command, shell=True, check=True, text=True, capture_output=True, cwd=main_path)
        print("Alembic initialization output:", result.stdout)
    except subprocess.CalledProcessError as e:
        print("Alembic initialization error:", e.stderr)
        
def setup_src_and_test_folders(src_path: Path, test_path: Path):
    create_folder(src_path)
    create_folder(test_path)
    create_file_with_content(test_path, INIT_FILE)
    create_file_with_content(test_path, "conftest.py", TEMPLATES["conftest.py"])



def setup_src_subfolders(src_path: Path):
    for folder_name in FOLDERS:
        folder_path = src_path / folder_name
        create_folder(folder_path)

        if folder_name != "other":
            create_file_with_content(folder_path, INIT_FILE)

        if folder_name == "base":
            create_file_with_content(folder_path, "db.py", TEMPLATES["db.py"])
            create_file_with_content(folder_path, "config.py", TEMPLATES["config.py"])

def main():
    current_path = Path.cwd()
    main_path = current_path / "main"
    src_path = main_path / "src"
    test_path = main_path / "test"

    setup_main_folder(main_path)
    setup_src_and_test_folders(src_path, test_path)
    setup_src_subfolders(src_path)

if __name__ == "__main__":
    typer.run(main)
