from setuptools import setup, find_packages

setup(
    name="fudstop3",  # Package name
    version="0.1.0",  # Initial version
    author="Chuck Dustin",
    author_email="chuckdustin12@gmail.com",
    description="An all-in-one market data API aggregator for analysis and real-time feeds.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),  # Automatically find package directories
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",  # Minimum Python version

    
)
