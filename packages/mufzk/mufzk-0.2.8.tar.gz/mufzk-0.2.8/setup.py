from setuptools import setup, find_packages

#  venv\Scripts\python.exe .\setup.py sdist bdist_wheel
setup(
    name="mufzk",
    version="0.2.8",
    packages=find_packages(),
    install_requires=[
        "numpy>=1.11.1",
        "scipy>=1.13.1"
    ],
)
