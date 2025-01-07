from setuptools import setup, Extension, find_packages
#from Cython.Build import cythonize
import os

#extensions = [
#    Extension("falconEDA.app", ["falconEDA/app.py"]),
#    Extension("falconEDA.utils", ["falconEDA/utils.py"]),
#    Extension("falconEDA.make_pptx", ["falconEDA/make_pptx.py"]),
#    Extension("falconEDA.main", ["falconEDA/main.py"]),
#]

setup(
    name="FalconEDA",  # Name of your package
    version="1.0.1",   # Package version
    author="Riley Heiman",
    license="GPL-3.0-or-later",
    #author_email="",
    description="A Streamlit-based app for fast and interactive exploratory data analysis",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    #url="https://github.com/Riley25/FalconEDA", 
    packages=find_packages(),
    #ext_modules=cythonize(extensions, language_level="3"),
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
            "falconEDA=run_app:run",  
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)

