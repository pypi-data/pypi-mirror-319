from setuptools import find_packages, setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='lor_gdp_tools',
    packages=find_packages(),
    version='1.2.6',
    description='This is a utility package designed to enable data scientitists and analysts to easily access GDP data within a python environment',
    long_description=long_description,
    long_description_content_type="text/markdown",    
    url="https://github.com/laingorourke/lor-gdp-tools",
    author="Damian Rumble <DRumble@laingorourke.com>"
)

### Python code to publish package ###
#python setup.py sdist bdist_wheel
#twine upload -u __token__ -p [PYPI API KEY - in ENV file] dist/*