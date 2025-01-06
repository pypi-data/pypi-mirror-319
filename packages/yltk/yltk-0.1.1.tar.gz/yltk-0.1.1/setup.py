from setuptools import setup, find_packages

setup (
    name="yltk",  # Name of your library
    version="0.1.1",  # Version of your library
    packages=find_packages(),  # Automatically find packages in your directory
    tests_require=["pytest"],  # Test dependencies
    test_suite="tests",  # Directory for tests
    author="Kolade Atanseiye",
    author_email="kolade.atanseiye@outlook.com",
    description="---",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/atanseiye/YLTK-library",  # GitHub repository URL
    classifiers=[  # Optional classifiers to help users find your library
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "openai",
    ],
)
