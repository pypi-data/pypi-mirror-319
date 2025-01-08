from setuptools import setup, find_packages

setup(
    name="auto_setup",
    version="0.1.0",
    author="Bekzod G'ulomov",
    author_email="pterest160@gmail.com",
    description="A Python package for creating folders, files, and initializing configurations",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/mypackage",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "fastapi", "typer", "sqlalchemy", "pydantic", "python-dotenv", "pytest", "alembic"
    ],
    python_requires=">=3.6",
)
