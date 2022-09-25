from setuptools import setup, find_packages

VERSION = '0.0.1' 
DESCRIPTION = 'Advanced Python Course Project: Search Engine'
# LONG_DESCRIPTION = ''

# Setting up
setup(
       # the name must match the folder name 'verysimplemodule'
        name="search_engine", 
        version=VERSION,
        author="Dechang Chen",
        author_email="math.dchen@gmail.com>",
        description=DESCRIPTION,
        # long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=[], # add any additional packages that 
        # needs to be installed along with your package. Eg: 'caer'
        
        keywords=['python', 'search engine'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ]
)