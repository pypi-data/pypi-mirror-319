from setuptools import setup, find_packages

setup(
    name="endoc",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "gql[requests]==3.5.0",
    ],
    description="Endoc SDK: A note-taking app SDK powered by LLMs",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Grigor Dochev",
    url="https://github.com/science-editor/endoc-python-sdk",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)