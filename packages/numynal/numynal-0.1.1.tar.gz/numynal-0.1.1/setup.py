from setuptools import find_packages, setup

setup(
    name="numynal",
    version="0.1.1",
    description="A comprehensive data anlysis library",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Affan Hamid",
    author_email="affanhamid007@gmail.com",
    url="https://github.com/affanhamid/numynal",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",
    install_requires=["pandas"],
)
