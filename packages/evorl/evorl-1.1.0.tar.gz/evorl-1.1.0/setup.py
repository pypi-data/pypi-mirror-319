from setuptools import setup, find_packages

# Read README for long description
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="evorl",
    version="1.1.0",
    author="Alex Zhang",
    author_email="zhangalex1237@gmail.com",
    description="An evolutionary reinforcement learning framework",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/zhangalex1/evorl",
    project_urls={
        "Documentation": "https://evorl.ai",
        "Bug Tracker": "https://github.com/zhangalex1/evorl/issues",
    },
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    python_requires=">=3.8",
    install_requires=[
        "torch>=1.8.0",
        "numpy>=1.19.0",
        "gymnasium>=0.26.0",
        "matplotlib>=3.3.0",
        "seaborn>=0.11.0",
    ],
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov>=2.0",
            "black>=22.0",
            "isort>=5.0",
            "flake8>=3.9",
            "mypy>=0.9",
            "build>=0.7.0",
            "twine>=3.4.2",
        ],
        "docs": [
            "sphinx>=4.0",
            "sphinx-rtd-theme>=1.0",
        ],
    }
)
