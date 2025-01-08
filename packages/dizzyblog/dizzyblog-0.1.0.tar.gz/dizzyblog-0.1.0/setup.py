from setuptools import setup, find_packages 



setup(
    name="DizzyBlog",  # Your package name
    version="0.1.0",    # Initial version
    description="A simple blog app",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Fiza Rafakat",
    author_email="fiza@example.com",
    url="https://github.com/fiza/my_project",
    packages=find_packages(), 
    python_requires=">=3.6",  
)
