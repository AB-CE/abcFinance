from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='abcFinance',
      version='0.1',
      description='',
      url='https://github.com/AB-CE/abcFinance',
      packages=['abcFinance'],
      long_description=long_description,
      long_description_content_type="text/markdown",
      zip_safe=True)
