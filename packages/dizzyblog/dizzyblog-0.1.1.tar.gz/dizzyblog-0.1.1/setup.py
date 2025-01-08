from setuptools import setup, find_packages

setup(
    name="dizzyblog",  # Package name (must be unique on PyPI)
    version="0.1.1",
    description="A simple blog management tool",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Your Name",
    author_email="your_email@example.com",
    url="https://github.com/FiZaRafakat/dizzyblog-python-cli",  
    license="MIT",
    packages=find_packages(),  # Automatically include all packages
    python_requires=">=3.6",
    entry_points={
        'console_scripts': [
            'dizzyblog = dizzyblog.main:main', 
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)

