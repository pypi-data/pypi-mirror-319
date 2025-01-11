from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="flux-agents",
    version="0.1.1",
    author="Christian de Frondeville, Arijit Nukala, Gubi Ganguly",
    author_email="your.email@example.com",
    description="Advanced AI Agent Framework with LLM integration",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/flux",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.9",
    install_requires=[
        # Storage + serialization
        "msgpack>=1.0.5",
        "zstandard",
        "pyarrow",
        "polars>=0.20.6",
        "numpy",
        "xmltodict>=0.13.0",
        "pyyaml>=6.0.1",
        
        # LLM + vector operations
        "google-generativeai",
        "hnswlib",
        "transformers",
        
        # Async operations
        "aiofiles",
        "aiohttp",
        
        # Visualization
        "plotly",
        
        # Monitoring
        "langfuse",
        
        # VCS
        "diff-match-patch",
        "patience",
        
        # Optional preview dependencies
        "pandas",
        "tabulate"
    ],
    extras_require={
        'torch': [
            "torch",
            "sentence-transformers[torch]>=2.5.0",
        ],
        'docs': [
            "sphinx>=7.1.2",
            "sphinx-rtd-theme>=1.3.0",
            "myst-parser>=2.0.0",
            "sphinx-autodoc-typehints>=1.25.2"
        ],
        'dev': [
            "pytest",
            "pytest-asyncio",
            "black",
            "isort",
            "mypy",
            "flake8"
        ]
    }
)