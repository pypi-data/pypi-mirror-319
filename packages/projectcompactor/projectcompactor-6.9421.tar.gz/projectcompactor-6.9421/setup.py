# setup.py

import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="projectcompactor",               # Your package name on PyPI
    version="6.9421",                      # The version you're publishing
    author="veppy",
    author_email="vonepern@gmail.com.com",
    description="A powerful, user-friendly Python tool to generate project trees and file contents (with MIME detection).",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/projectcompactor",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires=">=3.6",
    install_requires=[
        "tqdm>=4.0.0",
        "python-magic>=0.4.15",  # This ensures python-magic is installed
    ],
    entry_points={
        "console_scripts": [
            # 'projectcompactor' is the command user types
            # 'projectcompactor.cli:main' is the function that runs
            "projectcompactor=projectcompactor.cli:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)
