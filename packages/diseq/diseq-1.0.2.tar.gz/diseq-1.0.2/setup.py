import os
import urllib.request
from setuptools import setup, find_packages
from setuptools.command.install import install



setup(
    name="diseq",
    version="1.0.2",
    description="A tool for disease embeddings and queries",
    author="Christian Hoffmann",
    packages=find_packages(),
    install_requires=[
        "numpy",
        "pandas",
        "requests",
        "torch",
        "gensim",
        "langchain_community",
        "scipy",
        "scikit-learn",
        "tabulate",
        "tqdm",
        "transformers",
        "gdown"
    ],
    python_requires=">=3.8",
)


