from setuptools import setup, find_packages

setup(
    name="pytweet-selenium",                # Your library's name
    version="1.0.0",                  # Version number
    description="Get tweet content using selenium",  # Short description
    long_description=open("README.md").read(),  # Detailed description
    long_description_content_type="text/markdown",
    author="Alexander",               # Your name
    author_email="hellolightning321@gmail.com",
    url="https://github.com/AlexanderJiazx/pytweet.git",  # GitHub URL
    packages=find_packages(),         # Automatically find packages
    install_requires=[             # External dependencies
        'selenium',
        'bs4',
        'requests',                # Added 'click' for CLI functionality
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",          # Minimum Python version
)
