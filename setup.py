"""
Cmdflow
-------

A simple wrapper for creating shell pipelines inside python scripts

Theoretically, this can be used across platforms, but there are a few
conventions which do not translate well to Windows; i.e. `sudo` is difficult in
a system that does not use multiple simultaneous users.
"""

try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup, find_packages

setup(name="CmdFlow",
      version="dev",
      packages=find_packages(),
      include_package_data=True,
      author='Dan Colish',
      author_email='dcolish@gmail.com',
      description='A simple wrapper for creating shell pipelines',
      long_description=__doc__,
      zip_safe=False,
      platforms='any',
      license='MIT',
      url='https://github.com/dcolish/cmdflow',
      classifiers=[
        'Development Status :: 1 - Planning',
        'Environment :: Console',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 2.7',
        'Operating System :: Unix',
        ],
)
