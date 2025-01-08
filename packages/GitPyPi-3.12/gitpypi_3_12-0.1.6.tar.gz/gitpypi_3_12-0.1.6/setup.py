
from pathlib import Path

from setuptools import find_packages, setup

setup(
    name="GitPyPi_3.12",
    version="0.1.6",
    packages=find_packages(),
    install_requires=[
        'pytest>=7.0.0',
        'pytest',
        'replit==4.1.0',
        'black',
        'flake8',
        'build',
        'requests',
        'pyright',
        'toml',
        'pyyaml',
        'isort',
        'pyproject-flake8',
        'zipfile38==0.0.3'
    ],
    author="Joao Lopess",
    author_email="joaoslopes@gmail.com",
    description="",
    long_description=Path('README.md').read_text(),
    long_description_content_type="text/markdown",
    url="https://github.com/kairos-xx/GitPyPi_3.12",
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.11',
        'Operating System :: OS Independent',
        'Natural Language :: English',
        'Typing :: Typed',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    python_requires=">=3.11",
)
