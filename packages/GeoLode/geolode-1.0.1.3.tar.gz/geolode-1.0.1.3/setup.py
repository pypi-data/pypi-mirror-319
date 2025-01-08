from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
      name='GeoLode',
      version='1.0.1.3',
      author='Anchenry',
      description='Python package designed for efficient geospatial data analysis',
      url='',
      author_email='anchenry.h@gmail.com',
      long_description=long_description,
      long_description_content_type="text/markdown",
      license='MIT',
      packages=['geolode'],
      zip_safe=False
)