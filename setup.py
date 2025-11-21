"""
PySchedule setup configuration for pip installation.

Install in development mode:
    pip install -e .

Install from source:
    pip install .
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README for long description
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text(encoding="utf-8") if readme_file.exists() else ""

setup(
    name="pyschedule",
    version="1.0.0",
    author="PySchedule Development Team",
    author_email="pyschedule@example.com",
    description="A discrete-event simulation framework for evaluating real-time scheduling algorithms",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/pyschedule",
    project_urls={
        "Bug Reports": "https://github.com/yourusername/pyschedule/issues",
        "Documentation": "https://github.com/yourusername/pyschedule",
        "Source Code": "https://github.com/yourusername/pyschedule",
    },

    # Package configuration
    packages=find_packages(exclude=["tests", "tests.*", "output", "results", "claudedocs"]),
    py_modules=[
        "simple_simulator",
        "algorithms",
        "scenarios",
        "runner",
        "visualizer",
        "pyschedule_cli",
    ],

    # Python version requirement
    python_requires=">=3.7",

    # Dependencies
    install_requires=[
        "matplotlib>=3.5.0",
        "pandas>=1.3.0",
        "numpy>=1.21.0",
    ],

    # Optional dependencies for development
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "pytest-xdist>=3.0.0",
            "black>=22.0.0",
            "flake8>=4.0.0",
            "mypy>=0.950",
            "hypothesis>=6.0.0",
        ],
        "viz": [
            "seaborn>=0.11.0",
        ],
    },

    # Entry points for command-line scripts
    entry_points={
        "console_scripts": [
            "pyschedule=pyschedule_cli:main",
        ],
    },

    # Classifiers for PyPI
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Developers",
        "Topic :: Scientific/Engineering",
        "Topic :: System :: Distributed Computing",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],

    # Keywords for discovery
    keywords="scheduling real-time algorithms simulation discrete-event research",

    # Include additional files
    include_package_data=True,
    package_data={
        "": ["*.yaml", "*.yml", "*.md", "*.txt"],
    },

    # Project metadata
    license="MIT",
    platforms=["any"],
)
