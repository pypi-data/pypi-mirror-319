from setuptools import setup, Extension
from Cython.Build import cythonize

extensions = [
    Extension(
        "mathutilstest._core",  # Make sure this matches your new package name
        ["mathutilstest/_core.pyx"],
    )
]

setup(
    name="mathutilstest",
    version="0.1.1",
    description="Math utilities implemented in Cython",
    author="Your Name",
    author_email="your.email@example.com",
    packages=["mathutilstest"],
    ext_modules=cythonize(extensions),
    python_requires=">=3.7",
    install_requires=["cython>=0.29.21"],
)