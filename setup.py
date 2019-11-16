import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='wavebin',
    version='1.0',
    packages=['wavebin'],
    author="sam210723",
    author_email="pypi@vksdr.com",
    description="Keysight/Agilent oscilloscope waveform file converter",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sam210723/wavebin",
    install_requires = [],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Topic :: Utilities"
    ],
)
