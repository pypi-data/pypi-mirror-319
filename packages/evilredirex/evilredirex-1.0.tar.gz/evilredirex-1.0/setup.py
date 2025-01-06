from setuptools import setup, find_packages

# Read the contents of README.md
with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="evilredirex",  # Replace with your desired package name
    version="1.0",  # Start with a version 1.0.0
    author="SrilakiVarma",  # Replace with your name
    author_email="srilakivarma@gmail.com",  # Replace with your email
    description="A tool to test for open redirects and XSS vulnerabilities.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Evil-twinz/Evil-redirex",  # Replace with your GitHub repo URL
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        "requests",
        "selenium",
        "termcolor",
        "urllib3",
    ],
    entry_points={
        'console_scripts': [
            'evilredirex=evilredirex.main:main',
        ],
    },
    include_package_data=True,
)