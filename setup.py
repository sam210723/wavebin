import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='wavebin',
    version='2.3',
    packages=['wavebin'],
    author="sam210723",
    author_email="pypi@vksdr.com",
    description="Waveform capture viewer for Agilent, Keysight and Rigol oscilloscopes",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sam210723/wavebin",
    python_requires = '>3.6',
    install_requires = [
        'numpy',
        'pyqt5',
        'pyqtgraph'
    ],
    classifiers=[
        "Topic :: Scientific/Engineering :: Visualization",
        "Environment :: Console",
        "Environment :: X11 Applications :: Qt",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Development Status :: 5 - Production/Stable",
        "Natural Language :: English",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9"
    ]
)
