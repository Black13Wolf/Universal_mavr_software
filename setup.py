from setuptools import setup, find_packages
from mavrControl import __version__
from os.path import join
from os import walk
def search_help_files():
      base_path = join('mavrControl', 'doc')
      output = []
      for root, dirs, files in walk(base_path):
            for f in files:
                  if f.endswith('.html') or f.endswith('.css') or f.endswith('.png'):
                        output.append((root, [join(root, f)]))
      return output


setup(name='ums',
      version=__version__,
      description='Module of automatisation several tasks for MAVR SAO RAN',
      author='Anatoly Beskakotov',
      author_email='beskakotov.as@gmail.com',
      url='https://github.com/Black13Wolf/universal_mavr_software',
      packages=find_packages(),
      data_files=search_help_files(),
      include_package_data=True,
      install_requires=['PyQt5>=5.10', 'numpy>=1.14', 'scipy>=1.0', 'matplotlib>=2.1.2', 'pyqtgraph>=0.10', 'markdown2>=2.3'],
     )