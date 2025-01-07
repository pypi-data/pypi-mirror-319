from setuptools import setup, find_packages

setup(
    name="torchevent",
    version="0.0.2",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "torch",
        "tonic",
        "matplotlib",
        "tqdm",
        "pandas"
    ],
    extras_require={
        "dev": [
            "pytest",
            "pytest-cov",
        ],
    },
    entry_points={
        "console_scripts": [
            "torchevent=torchevent.main:main",
        ],
    },
)