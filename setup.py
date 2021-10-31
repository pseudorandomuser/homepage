from setuptools import find_packages, setup

setup(
    name='app',
    version='0.0.1',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'uwsgi>=2.0.20',
        'flask>=2.0.2',
        'flask_mongoengine>=1.0.0',
        'pyyaml>=6.0',
        'types-PyYAML>=6.0.0'
    ],
)
