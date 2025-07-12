from setuptools import setup, find_packages
import os


def get_long_description():
    with open(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "README.md"),
        encoding="utf8",
    ) as fp:
        return fp.read()


setup(
    name="vidtoolz",
    version="0.1.4",
    description="CLI tools for editing videos in python. A plugin based approach.",
    packages=find_packages(),
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    entry_points={
        "console_scripts": ["vid = vidtoolz.cli:main", "vidtoolz = vidtoolz.cli:main"]
    },
    install_requires=["pluggy", "moviepy", "imageio-ffmpeg", "pip"],
    python_requires=">=3.9",
    author="Sukhbinder Singh",
    url="https://github.com/sukhbinder/vidtoolz",
    extra_require={
        "test": ["pytest"],
    },
    project_urls={
        "Documentation": "https://sukhbinder.wordpress.com",
        "Issues": "https://github.com/sukhbinder/vidtoolz/issues",
        "CI": "https://github.com/sukhbinder/vidtoolz/actions",
        "Changelog": "https://github.com/sukhbinder/vidtoolz/releases",
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Database",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
    ],
)
