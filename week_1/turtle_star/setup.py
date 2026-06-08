"""Package setup for turtle_star."""
from glob import glob

from setuptools import find_packages, setup

package_name = 'turtle_star'

setup(
    name=package_name,
    version='0.0.1',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
         ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + '/launch',
         glob('launch/*.launch.py')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Janosch Bajorath',
    maintainer_email='j.bajorath@uni-muenster.de',
    description='Drives turtlesim to draw a five-pointed star.',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'star_node = turtle_star.star_node:main',
        ],
    },
)
