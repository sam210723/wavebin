import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='wavebin',
    version='3.0',
    packages=['wavebin', 'wavebin.interface', 'wavebin.vendor'],
    entry_points={
        'console_scripts': [
            'wavebin=wavebin.__main__:main',
        ]
    },
    author="sam210723",
    author_email="pypi@vksdr.com",
    description="Oscilloscope waveform capture viewer",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sam210723/wavebin",
    python_requires = '>3.6',
    install_requires = [
        'appdirs>=1.4.4',
        'numpy>=1.21.0',
        'pyqt5>=5.15.0',
        'matplotlib>=3.4.3'
        #'pyqtgraph>=0.12.3',
        #'vispy>=0.9.3',
        'qtawesome>=1.1.0',
        'requests>=2.24.0'
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
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10"
    ]
)
