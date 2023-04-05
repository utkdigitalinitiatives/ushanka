from setuptools import setup, find_packages

with open("README.md", "r") as read_me:
    long_description = read_me.read()


setup(
    name="Ushanka",
    description="Documentation relating to born digital preservation at the University of Tennessee Libraries",
    long_description=long_description,
    long_description_content_type="text/markdown",
    version="0.0.1",
    author="Mark Baggett",
    author_email="mbagget1@utk.edu",
    maintainer_email="mbagget1@utk.edu",
    url="https://github.com/utkdigitalinitiatives/ushanka",
    packages=find_packages(),
    install_requires=[
        "requests>=2.28.2",
        "python-magic>=0.4.27",
        "python-dotenv>=1.0.0",
        "xmltodict>=0.13.0",
        "bitmath>=1.3.3.1",
        "pyyaml>=6.0",
        "sphinxcontrib-mermaid==0.8.1",
    ],
    extras_require={
        "docs": [
            "sphinx >= 5.0.2",
            "sphinx-rtd-theme >= 1.0.0",
            "sphinxcontrib-mermaid==0.8.1",
        ]
    },
    classifiers=[
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python :: 3.8",
        "Operating System :: OS Independent",
        "Topic :: Multimedia :: Graphics :: Presentation",
    ],
    keywords=["libraries", "documentation", "born digital", "preservation"],
)