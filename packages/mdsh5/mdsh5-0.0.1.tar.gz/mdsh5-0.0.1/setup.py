from setuptools import setup


with open("README.md", "r") as fh:
    long_description = fh.read()

version = '0.0.0'
short_des = ('A higher level python package that uses mdsthin to read MDSPlus data '
             + 'and store it in hdf5 formate for easy caching, viewing, distribution, '
             + 'and analysis.')
dwnld_url = ('https://github.com/anchal-physics/mdsh5/archive/refs/tags/v'
             + version + '.tar.gz')

# Chose either "3 - Alpha" or "4 - Beta"
# or "5 - Production/Stable" as the current state of your package
classifiers = ['Development Status :: 3 - Alpha',
               'Intended Audience :: Developers',
               'Topic :: Software Development :: Build Tools',
               'License :: OSI Approved :: Apache-2.0 license',
               'Programming Language :: Python :: 3']

with open('./mdsh5/__init__.py', 'r') as f:
    initLines = f.readlines()

for ii, line in enumerate(initLines):
    if '__version__' in line:
        initLines[ii] = '__version__ = \'' + version + '\'\n'

with open('./mdsh5/__init__.py', 'w') as f:
    f.writelines(initLines)

setup(name='mdsh5',
      packages=['mdsh5'],
      version=version,
      license='LICENSE',
      description=short_des,
      long_description=long_description,
      long_description_content_type="text/markdown",
      author='Anchal Gupta',
      author_email='anchal.physics@gmail.com',
      url='https://github.com/anchal-physics/mdsh5',
      download_url=dwnld_url,
      keywords=['MDSPlus', 'HDF5'],
      install_requires=['h5py', 'PyYAML', 'mdsthin'],
      classifiers=classifiers,
      scripts=['bin/read_mds'])

