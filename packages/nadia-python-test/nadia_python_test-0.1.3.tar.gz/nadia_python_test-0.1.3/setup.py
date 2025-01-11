from setuptools import setup, find_packages

setup(
    name="nadia-python-test",  # Matches your PyPI project name
    version="0.1.3",
    author="Nadia Hamdi",
    author_email="your_email@example.com",
    description="A test package by Nadia.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/nadia-python-test",  # Replace with your GitHub repo link
    packages=find_packages(),  # Automatically find and include 'nadia_python_test'
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
