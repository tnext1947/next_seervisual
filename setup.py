
## ! DO NOT MANUALLY INVOKE THIS setup.py, USE CATKIN INSTEAD
## See http://ros.org/doc/api/catkin/html/user_guide/setup_dot_py.html

from distutils.core import setup
from catkin_pkg.python_setup import generate_distutils_setup
from setuptools import setup

# fetch values from package.xml
setup_args = generate_distutils_setup(
    packages=['robot_visual_api'],
    # packages=['next_seerrobot', 'socketio', 'engineio', 'engineio.async_drivers', 'bidict'],
    # packages=['socketio'],
    install_requires=[
          'markdown',
      ],
    package_dir={'': 'scripts'}
)

setup(**setup_args)