from setuptools import setup

package_name = 'rmc_to_imu'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='mcity',
    maintainer_email='rdlrobot@umich.edu',
    description='Takes in NMEA sentences, parses RMC messages from them, and converts it to an absolute position IMU.',
    license='MIT License',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'rmc_to_imu = rmc_to_imu.rmc_to_imu:main'
        ],
    },
)
