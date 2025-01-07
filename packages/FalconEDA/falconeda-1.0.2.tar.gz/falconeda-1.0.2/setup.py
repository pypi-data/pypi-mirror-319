from setuptools import setup, Extension, find_packages
import os

setup(
    name="FalconEDA", 
    version="1.0.2", 
    author="Riley Heiman",
    license="GNU General Public License v3.0 or later",
    description="A Streamlit-based app for fast and interactive exploratory data analysis",
    long_description=open("README.md",  encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "streamlit>=1.0",
        "pandas>=1.3",
        "numpy>=1.21",
        "altair>=4.2",
        "matplotlib",
        "openpyxl",
        'python-pptx', 
        'vl-convert-python'
    ],
    entry_points={
        "console_scripts": [
            "FalconEDA=run_app:run",  
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7"
)

