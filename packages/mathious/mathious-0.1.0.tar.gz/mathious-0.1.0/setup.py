from setuptools import setup, find_packages

setup(
    name="mathious",  
    version="0.1.0",  
    author="samanda Andres",
    author_email="samandaAndre@proton.me",
    description="A simple math library",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
