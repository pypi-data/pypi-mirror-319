from setuptools import setup, find_packages

setup(
    name="TBBS",
    version="0.1.0",
    description="The TBBS Module",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Raghav and Ayush",
    author_email="your.email@example.com",
    url="https://github.com/yourusername/Slize",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)