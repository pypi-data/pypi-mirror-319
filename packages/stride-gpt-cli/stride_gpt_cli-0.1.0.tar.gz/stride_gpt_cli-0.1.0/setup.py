from setuptools import setup, find_packages

# Read the contents of README.md
with open("src/client/README.md", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="stride-gpt-cli",
    version="0.1.0",
    description="CLI for the STRIDE GPT Pro threat modeling tool",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Matthew Adams",
    author_email="matt@cyberthreat.co",
    packages=find_packages(where="src", include=["client*"]),
    package_dir={"": "src"},
    install_requires=[
        "click>=8.0.0",
        "rich>=10.0.0",
        "httpx>=0.24.0",
        "python-dotenv>=1.0.0",
        "pydantic>=2.0.0"
    ],
    entry_points={
        "console_scripts": [
            "stride-gpt=client.cli:cli",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Security",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.8",
) 