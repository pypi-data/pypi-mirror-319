from setuptools import setup, find_packages

setup(
    name="llmcaller",
    version="1.0.0",
    description="Python SDK for LLMCaller - A unified interface for LLM providers",
    author="",
    author_email="",
    packages=find_packages(),
    install_requires=[
        "aiohttp>=3.8.0",
        "requests>=2.28.0",
        "sseclient-py>=1.7.2",
        "typing_extensions>=4.5.0",
    ],
    python_requires=">=3.7",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)
