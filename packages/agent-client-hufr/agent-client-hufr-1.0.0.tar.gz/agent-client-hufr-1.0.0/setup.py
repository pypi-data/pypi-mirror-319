from setuptools import setup, find_packages

setup(
    name="agent-client-hufr",  # Package name on PyPI
    version="1.0.0",  # Initial version
    description="A Python client library for communicating with the Flask server",
    long_description=open("README.md", "r").read(),
    long_description_content_type="text/markdown",
    author="Taha",
    author_email="tghara1@lsu.edu",
    url="https://github.com/TahaW863/agent-client",  # GitHub repo URL
    packages=find_packages(),  # Automatically discover all packages in the 'agent/' directory
    install_requires=["requests"],  # Dependencies
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
