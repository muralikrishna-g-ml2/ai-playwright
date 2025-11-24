from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="ai-playwright",
    version="0.1.0",
    author="Murali Krishna",
    author_email="muralikrishna.g.ml2@gmail.com",
    description="AI-enhanced Playwright framework with self-healing test capabilities",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/muralikrishna-g-ml2/ai-playwright",
    packages=find_packages(exclude=["tests*"]),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Testing",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.8",
    install_requires=[
        "playwright>=1.40.0",
        "pytest>=7.0.0",
        "google-generativeai>=0.3.0",
        "python-dotenv>=1.0.0",
    ],
    extras_require={
        "dev": [
            "pytest-playwright>=0.4.0",
        ],
        "openai": [
            "openai>=1.0.0",
        ],
        "anthropic": [
            "anthropic>=0.8.0",
        ],
        "ollama": [
            "requests>=2.0.0",
        ],
        "all-providers": [
            "openai>=1.0.0",
            "anthropic>=0.8.0",
            "requests>=2.0.0",
        ],
    },
)
