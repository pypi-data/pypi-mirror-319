from setuptools import setup, find_packages

setup(
    name="streamix",  # Your package name
    version="0.2",  # Version of your package
    packages=find_packages(),  # Automatically find all packages in your project
    install_requires=[  # List of dependencies
        "yt-dlp",
    ],
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    author="Your Name",
    author_email="your.email@example.com",
    url="https://github.com/username/streamix",  # Link to GitHub
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
