from setuptools import find_packages, setup

setup(
    name="percolate",
    version="0.0.1",
    packages=find_packages(),
    install_requires=["numpy", "matplotlib"],
    entry_points={
        "console_scripts": [
            "simulate = percolate.__main__:main",
        ],
    },
)
