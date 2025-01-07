from setuptools import setup, find_packages
import os

# Read long description from README.md
long_description = ""
if os.path.exists("README.md"):
    with open("README.md", "r", encoding="utf-8") as fh:
        long_description = fh.read()

setup(
    name="spectral_sound_analysis",
    version="1.0.0",
    description="A Python package for performing spectral analysis, audio signal processing, and related computations.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Luís Miguel da Luz Raimundo",
    author_email="lmr.2020@outlook.pt",
    url="https://github.com/LuisMRaimundo/Spectral_Sound_Analysis",
    license="Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International License",
    packages=find_packages(),
    install_requires=[
        "numpy>=1.18.0",
        "scipy>=1.4.0",
        "matplotlib>=3.2.0",
        "pandas>=1.1.0",
        "librosa>=0.8.0",
        "PyQt5>=5.15.0",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "License :: Other/Proprietary License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    keywords="spectral analysis, audio processing, signal processing, sound analysis",
)





