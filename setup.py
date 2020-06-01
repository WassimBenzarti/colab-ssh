import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="colab_ssh",
    version="0.2.57",
    author="Wassim Benzarti",
    author_email="m.wassim.benzarti@gmail.com",
    description="Google colab SSH connector",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/WassimBenzarti/colab-ssh-connector.git",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
