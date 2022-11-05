from setuptools import setup

setup(
    name='Asset selector',
    version='1.0',
    long_description=__doc__,
    packages=['assetselector'],
    include_package_data=True,
    zip_safe=False,
    install_requires=['Flask']
)