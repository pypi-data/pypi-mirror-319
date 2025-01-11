import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="py-git-backup", 
    version="0.0.2",
    author="Richard Peschke",
    author_email="peschke@hawaii.edu",
    description="build scripts for firmware projects",
    long_description="long_description",
    long_description_content_type="text/markdown",
    url="",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[

    ],
    python_requires='>=3.8',
    
    entry_points = {
        'console_scripts': ['pygitup=pygitup.main_pygitup:main_pygitup'],
    }
)
