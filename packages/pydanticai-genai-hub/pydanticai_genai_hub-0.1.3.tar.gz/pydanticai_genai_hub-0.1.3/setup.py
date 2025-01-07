from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="pydanticai-genai-hub",
    version="0.1.3",
    author="Gunter",
    description="SAP Generative AI Hub: Pydantic AI models for various LLM providers",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/skye0402/pydanticai-genaihub",
    packages=find_packages(include=["pydanticai_genai_hub", "pydanticai_genai_hub.*"]),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.12"
    ],
    python_requires=">=3.12",
    install_requires=[
        "pydantic>=2.0.0",
        "pydantic-ai>=0.0.17",
        "typing-extensions>=4.0.0",
        "httpx>=0.24.0",
        "generative-ai-hub-sdk>=4.0.0"
    ],
    extras_require={
        "anthropic": ["anthropic>=0.3.0"],
        "openai": ["openai>=1.0.0"],
        "all": [
            "anthropic>=0.3.0",
            "openai>=1.0.0",
        ],
    }
)
