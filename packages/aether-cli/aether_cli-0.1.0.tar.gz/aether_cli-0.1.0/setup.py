from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="aether-cli",
    version="0.1.0",
    keywords="ai",
    author="AirTouch666",
    author_email="me@airtouch.top",
    description="A command-line interface for interacting with various AI models.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/AirTouch666/aether",
    project_urls={
        "Bug Tracker": "https://github.com/AirTouch666/aether/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=find_packages(),
    python_requires=">=3.7",
    install_requires=[
        "click>=8.0.0",
        "openai>=0.27.0",
        "google-generativeai>=0.3.0",
        "aiohttp>=3.8.0",
        "websockets>=10.0",
        "requests>=2.25.0",
        "halo>=0.0.31",
        "certifi>=2021.5.30"
    ],
    entry_points={
        "console_scripts": [
            "ask=aether.cli:main",
        ],
    },
) 