import os
import sys
import shutil
from setuptools import setup, find_packages, find_namespace_packages
from setuptools.command.install import install

# Change name to "astroraytrace" when you want to
#  load to PYPI
pypiname = 'astroraytrace'

setup(name="astroraytrace",
      version='1.0.3',
      description='Astronomical optics ray tracing',
      author='David Nidever',
      author_email='dnidever@montana.edu',
      url='https://github.com/dnidever/raytrace',
      requires=['numpy','astropy(>=4.0)','scipy'],
      zip_safe = False,
      include_package_data=True,
      packages=find_namespace_packages(where="python"),
      package_dir={"": "python"}
)
