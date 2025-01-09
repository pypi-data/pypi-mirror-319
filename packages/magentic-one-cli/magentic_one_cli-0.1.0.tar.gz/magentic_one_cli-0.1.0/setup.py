from setuptools import setup, find_packages

setup(
    name="magentic-one-cli",
    version="0.1.0",
    description="A CLI tool for demonstration.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Your Name",
    author_email="youremail@example.com",
    url="https://github.com/yourusername/magentic-one-cli",
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'magentic-one-cli=magentic_one_cli.main:main',
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
