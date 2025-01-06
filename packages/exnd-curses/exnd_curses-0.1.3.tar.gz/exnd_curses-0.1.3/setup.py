from setuptools import setup, find_packages 
import platform

setup(
    name="exnd-curses",
    version="0.1.3",
    description="Simple use of curses.",
    author="Shantanu Kor",
    author_email="kor.shantanu1@gmail.com",
    url="https://github.com/shantanu-kor/exnd-curses.git",
    packages=find_packages(),
    install_requires=[],
    extras_require={
	"windows": ["windows-curses"],
	"linux": ["curses"],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)