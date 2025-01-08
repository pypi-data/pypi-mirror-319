from setuptools import setup, find_packages

setup(
    name="gtools2",
    version="0.1",
    packages=find_packages(),
    author="Gamma",
    author_email="Gamma.scratch@gmail.com",
    description="A package that includes almost all built-in tools",
    url="https://github.com/Gamma7113131/gtools",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    entry_points={
        'console_scripts': [
            'gtools=gtools.cli:main',
        ],
    },
)