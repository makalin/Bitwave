from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="bitwave",
    version="1.0.0",
    author="Bitwave Team",
    author_email="contact@bitwave.audio",
    description="Next-Gen Multi-Channel Audio Format",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/makalin/Bitwave",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Multimedia :: Sound/Audio",
    ],
    python_requires=">=3.8",
    install_requires=[
        "numpy>=1.21.0",
        "soundfile>=0.10.3",
    ],
    entry_points={
        "console_scripts": [
            "bitwave=bitwave.cli:main",
        ],
    },
) 