from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
    
setup(
    name="torchevent",
    version="0.0.3",
    author="seokhun.jeon",
    author_email="devcow85@gmail.com",
    description="A PyTorch library for event-based data processing",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url= "https://github.com/devcow85/torchevent",
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
    classifiers=[
        "Development Status :: 4 - Beta", 
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
    ],
)