from setuptools import setup, find_packages
from mavrControl import __version__
setup(name='linux_mavr_software',
      version=__version__,
      description='Module of automatisation several tasks for MAVR SAO RAN',
      author='Anatoly Beskakotov',
      author_email='beskakotov.as@gmail.com',
      url='https://github.com/Black13Wolf/linux_mavr_module',
      packages=find_packages(),
      install_requires=['PyQt5>=5.10', 'numpy>=1.14', 'scipy>=1.0', 'matplotlib>=2.1.2', 'pyqtgraph>=0.10', 'markdown2>=2.3'],
     )