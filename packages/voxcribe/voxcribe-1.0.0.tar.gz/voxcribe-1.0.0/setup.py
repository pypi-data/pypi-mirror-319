from setuptools import setup, find_packages

setup(
    name="voxcribe",
    version="1.0.0",
    description="A lightweight audio transcription tool using speech recognition.",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="Vedant Barhate",
    author_email="vedant.barhate27@example.com",
    url="https://github.com/VedantBarhate/voxcribe",
    license="MIT",
    packages=find_packages(),
    install_requires=[
        "speechrecognition",
        "pydub",
        "tqdm",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
