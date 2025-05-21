
from setuptools import setup, find_packages

setup(
    name='momo_zambia',
    version='1.0.0',
    description='ERPNext App for MTN MoMo Zambia Integration',
    author='Miyanda R. Hakooma',
    author_email='mhakooma@antares.co.zm',
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    install_requires=['frappe>=15.0.0'],
)
