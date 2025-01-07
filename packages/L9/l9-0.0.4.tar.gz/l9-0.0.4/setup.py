from setuptools import setup, find_packages

VERSION = "0.0.4"
DESCRIPTION = "L9 Module"
LONG_DESCRIPTION = "A package that allows you to display the L9 in the console, advertise the L9 services and transform a message into an L9 message."

setup(
        name="L9", 
        version=VERSION,
        author="Ehrakis",
        author_email="clement.gd03@gmail.com",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=[], 
        keywords=['python', 'L9'],
        classifiers= [
            "Development Status :: 5 - Production/Stable",
            "Intended Audience :: Other Audience",
            "Programming Language :: Python :: 3",
            "Operating System :: Microsoft :: Windows",
        ],
        project_urls={
            "GitHub": "https://github.com/ehrakis/L9"
        }
)