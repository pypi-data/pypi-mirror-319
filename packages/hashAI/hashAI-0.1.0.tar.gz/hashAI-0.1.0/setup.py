from setuptools import setup, find_packages

setup(
    name="hashAI",
    version="0.1.0",
    description="A powerful SDK for building AI assistants with RAG capabilities.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Rakesh",
    author_email="rakeshsahoo689@gmail.com",
    url="https://github.com/Syenah/opAI",
    packages=find_packages(),
    install_requires=[
        "openai",
        "anthropic",
        "groq",
        "langchain",
        "faiss-cpu",  # For vector storage
        "pydantic",   # For data validation
        "requests",   # For web tools
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "opai=opai.cli.main:main",
        ],
    },
)