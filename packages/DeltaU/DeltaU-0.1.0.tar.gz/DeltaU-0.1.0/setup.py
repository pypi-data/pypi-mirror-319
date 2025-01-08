from setuptools import setup, find_packages

setup(
    name="DeltaU",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "pandas>=1.0.0",
        "matplotlib>=3.0.0",
        "numpy>=1.18.0",
    ],
    description="A flexible backtesting package with customizable tear sheets",
    author="Julian Fortis",
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
