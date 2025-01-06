import os
from setuptools import setup, find_packages
from setuptools.command.build_ext import build_ext

# Package Metadata
VERSION = '0.0.0'
DESCRIPTION = 'statarb'
LONG_DESCRIPTION = 'stat ... arb ...'

# Setup Configuration
setup(
    name="starbie",
    version=VERSION,
    author="Robert Stanton",
    author_email="robertmstanton@proton.me",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    packages=find_packages(),  # Automatically find 'dolfin' package
    install_requires=[
        # 'numpy',
        # 'scipy',
        # 'pandas',
        # 'mplfinance',
        # 'yfinance',
        # 'pybind11'
    ],
    # cmdclass={"build_ext": build_ext},
    zip_safe=False,
    keywords=['finance', 'python', 'quant', 'statistical arbitrage',
              'mean reversion'],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.10',
)
