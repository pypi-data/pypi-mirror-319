from setuptools import setup, find_packages

setup(
    name="liebniz",
    version="1.0.0",
    description="Leibniz Secure Algorithm (LSA) implementation",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Akinsunlade Marvelous",
    author_email="akinmarvelous2022@gmail.com",
    url="https://github.com/Marvex18/leibniz",
    packages=find_packages(),
    install_requires=[
        "numpy",
    ],
    python_requires=">=3.6",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    include_package_data=True,
)
