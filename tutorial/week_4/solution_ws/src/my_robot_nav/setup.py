from setuptools import find_packages, setup

package_name = 'my_robot_nav'

setup(
    name=package_name,
    version='0.0.1',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    tests_require=['pytest'],
    zip_safe=True,
    entry_points={
        'console_scripts': [
            'obstacle_nav = my_robot_nav.obstacle_nav:main',
            'maze_nav = my_robot_nav.maze_nav:main',
        ],
    },
)
