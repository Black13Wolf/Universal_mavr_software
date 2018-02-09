from distutils.core import setup
from mavrControl import __version__
setup(name='linux_mavr_software',
      version=__version__,
      description='Module of automatisation several tasks for MAVR SAO RAN',
      author='Anatoly Beskakotov',
      author_email='beskakotov.as@gmail.com',
      url='https://github.com/Black13Wolf/linux_mavr_module',
      packages=['mavrControl',],
      install_requires=['mavr_module', 'numpy', 'scipy', 'matplotlib', 'pyqtgraph'],
      dependency_links=['git+https://github.com/black13wolf/mavr_module.git'],
     )