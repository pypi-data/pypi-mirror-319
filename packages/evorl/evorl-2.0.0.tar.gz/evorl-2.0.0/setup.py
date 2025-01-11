from setuptools import setup, find_packages
from pathlib import Path

# Read README for long description
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="evorl",
    version="2.0.0",
    author="Alex Zhang",
    author_email="zhangalex1237@gmail.com",
    description="An evolutionary reinforcement learning framework",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/zhangalex1/evorl",
    project_urls={
        "Documentation": "https://evorl.ai",
        "Bug Tracker": "https://github.com/zhangalex1/evorl/issues",
        "Source Code": "https://github.com/zhangalex1/evorl",
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    keywords="reinforcement-learning, evolutionary-algorithms, deep-learning, pytorch, rl",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
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
        ],
        "docs": [
            "sphinx>=4.0",
            "sphinx-rtd-theme>=1.0",
        ],
    },
    include_package_data=True,
)