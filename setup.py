from distutils.core import setup

setup(name='linux_mavr_software',
      version='0.0.1a',
      description='Module of automatisation several tasks for MAVR SAO RAN',
      author='Anatoly Beskakotov',
      author_email='beskakotov.as@gmail.com',
      url='https://github.com/Black13Wolf/linux_mavr_module',
      packages=['mavr-control',],
      install_requires=['mavr_module'],
      dependency_links=['git+https://github.com/black13wolf/mavr_module.git'],
     )