# setup.py
from setuptools import setup, find_packages

setup(
    name="DeSlin",
    version="0.2",
    packages=find_packages(),
    install_requires=[
        # Lista de dependencias si las hay
    ],
    author="Tu Nombre",
    author_email="abraham.gu1996@gmail.com",
    description="Una librería de ejemplo llamada DeSlin",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/tu_usuario/DeSlin",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
