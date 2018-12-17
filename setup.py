import re
from os.path import join, dirname
from setuptools import setup, find_packages

# reading package version (same way the sqlalchemy does)
with open(join(dirname(__file__), 'extractor', '__init__.py')) as v_file:
    package_version = re.compile(r".*__version__ = '(.*?)'", re.S).match(v_file.read()).group(1)


dependencies = [
    'numpy',
    'opencv-python',
]


setup(
    name="extractor",
    version=package_version,
    author="Shiva Nouri",
    author_email="shiva@carrene.com",
    install_requires=dependencies,
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'extractor = extractor.main:file_reader'
        ]
    },
    packages=find_packages(),
)
