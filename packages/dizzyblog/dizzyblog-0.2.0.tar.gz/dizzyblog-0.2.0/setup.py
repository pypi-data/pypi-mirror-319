from setuptools import setup, find_packages

setup(
    name="dizzyblog",  # Unique package name
    version="0.2.0",  # Initial version
    author="Your Name",
    author_email="your_email@example.com",
    description="A simple blogging CLI application.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/dizzyblog",  # Your GitHub repo
    packages=find_packages(),  # Automatically finds all packages
    include_package_data=True,  # Includes non-code files
    install_requires=[],  # Add dependencies here (if any)
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        "console_scripts": [
            "dizzyblog=dizzyblog.main:main",  # CLI command
        ],
    },
    python_requires=">=3.6",  # Minimum Python version
)
