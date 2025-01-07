from setuptools import setup, find_packages

setup(
    name="pipcherry",                     # Package name (used in pip install)
    version="0.1.0",                       # Package version
    author="Your Name",
    author_email="your_email@example.com",
    description="A simple Python package",
    long_description=open("README.md").read(),  # Optional: README content
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/pipcherry",  # GitHub or project URL
    packages=find_packages(),             # Automatically find and include packages
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',               # Minimum Python version
    install_requires=[],                   # Optional: Dependencies
)
