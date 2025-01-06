from setuptools import setup, find_packages

setup(
    name="fucking-read",
    version="0.1.3",
    description="Used exnd-curses to output file content.",
    author="Shantanu Kor",
    author_email="kor.shantanu1@gmail.com",
    url="https://github.com/shantanu-kor/fread.git",
    packages=find_packages(),
    install_requires=["exnd-curses"],
    entry_points={
        "console_scripts": [
            "read=fread.read",
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)