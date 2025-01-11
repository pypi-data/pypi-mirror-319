from setuptools import setup, find_packages
from pathlib import Path 

# Read long description from the README.md file
with open("README.md", "r") as fh:
    long_description = fh.read()

# Read requirements from requirements.txt
with open("requirements.txt", "r") as f:
    install_requires = f.read().splitlines()
    
this_directory = Path(__file__).parent
setup(
    name="anticp3",  # Replace with your package name
    version="1.1",  # Initial version
    author="GPS Raghava",
    author_email="raghava@iiitd.ac.in",
    description="AntiCP3 : Prediction of Anticancer Proteins",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/raghava/anticp3",  # Replace with your repo URL if hosting
    packages=find_packages(),  # Automatically finds submodules
    include_package_data=True,  # Includes files in MANIFEST.in
    package_data={
        'anticp3': [],
    },
    zip_safe=False,
    install_requires=install_requires,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6", # Dependencies
    entry_points={  # Entry point for the command line tool
        "console_scripts": [
            "anticp3=anticp3.anticp3:main",  # Runs anticp3.py's main code block
        ],
    },
    license="MIT"
)
