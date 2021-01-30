import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='wavebin',
    version='1.3',
    packages=['wavebin'],
    author="sam210723",
    author_email="pypi@vksdr.com",
    description="Waveform capture viewer for Keysight oscilloscopes",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sam210723/wavebin",
    install_requires = [
        'numpy',
        'pyqt5',
        'pyqtgraph'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Utilities"
    ],
)
