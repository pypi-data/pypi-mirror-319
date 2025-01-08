from setuptools import setup, find_packages

setup(
    name="cli_veripy",  # Replace with your package name
    version="1.1.9",
    description="A CLI Arguments verifier.",
    long_description=open("README.md").read(),  # Optional: Read from README.md
    long_description_content_type="text/markdown",  # Markdown format
    author="William L.",
    author_email="william.lim@csu.fullerton.edu",
    url="https://github.com/FrewtyPebbles/Python-CLI-Argument-Parser",  # Replace with your repo URL
    license="MIT",  # Or your preferred license
    packages=find_packages(),  # Automatically find sub-packages
    install_requires=[],  # List your dependencies here
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.10',  # Specify Python version compatibility
)