import os
import urllib.request
from setuptools import setup, find_packages
from setuptools.command.install import install

URL_EMBEDDINGS = "https://drive.google.com/file/d/1dT2nfKi_zTJ0fFibdhLQijqgH9adjgIx/view?usp=sharing"
URL_DISEASES = "https://drive.google.com/file/d/1E0CYr3f1F55KF1bVbxkLB22Kd_2pGiUP/view?usp=sharing"
URL_NODE2VEC = "https://drive.google.com/file/d/1SyiLB2uimJ2MqPU8f7SsLrhMw4xVkcgI/view?usp=sharing"


DATA_DIR = os.path.join(os.path.dirname(__file__), "diseq", "diseq_data")
EMBEDDINGS_PATH = os.path.join(DATA_DIR, "embeddings.pickle")
DISEASES_PATH = os.path.join(DATA_DIR, "diseases.pickle")
NODE2VEC_PATH = os.path.join(DATA_DIR, "node2vec_gene_model")


def download_file(url, dst_path):
    """
    Download file from `url` to `dst_path`,
    always overwriting (redownloading) to ensure latest data.
    """
    print(f"Downloading {url} -> {dst_path}")
    urllib.request.urlretrieve(url, dst_path)
    print("Download complete.")


class CustomInstall(install):
    """
    Custom install command to download data files upon install or upgrade.
    """
    def run(self):
        # Run the standard install process first
        super().run()

        # Ensure our data folder exists
        os.makedirs(DATA_DIR, exist_ok=True)

        # Download each file.
        # In a more advanced setup, you could check remote ETags or last-modified
        # timestamps to see if the file truly changed. Here we always overwrite.
        download_file(URL_EMBEDDINGS, EMBEDDINGS_PATH)
        download_file(URL_DISEASES, DISEASES_PATH)
        download_file(URL_NODE2VEC, NODE2VEC_PATH)


setup(
    name="diseq",
    version="0.2.0",
    description="A tool for disease embeddings and queries",
    author="Your Name",
    packages=find_packages(),  # This should find the 'diseq' package automatically
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
    ],
    cmdclass={
        # Override the default 'install' command with our custom class
        'install': CustomInstall,
    },
    python_requires=">=3.8",
)


