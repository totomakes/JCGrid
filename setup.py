from setuptools import setup

setup(
    name='Kid Gen',
    version='1.0',
    long_description=__doc__,
    packages=['kidgen'],
    include_package_data=True,
    zip_safe=False,
    install_requires=['Flask']
)