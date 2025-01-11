from setuptools import setup, find_packages

setup(
    name='stalse_functions',
    version='0.1',
    packages=['stalse_functions'],
    install_requires=[
        'pandas_gbq',
        'pandas',
        'flask',
        'google-cloud-storage',
        'google-cloud-secret-manager'
    ],
)