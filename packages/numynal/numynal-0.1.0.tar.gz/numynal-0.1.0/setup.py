from setuptools import find_packages, setup

setup(
    name="numynal",  # Replace with your project name
    version="0.1.0",  # Replace with your version
    description="A comprehensive data anlysis library",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Your Name",
    author_email="your.email@example.com",
    url="https://github.com/yourusername/myproject",  # Project URL
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",  # Specify minimum Python version
    install_requires=[  # Add dependencies here
        "numpy",  # Example
    ],
)
