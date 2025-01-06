from setuptools import setup, find_packages

setup(
    name='mysql_to_excel',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'mysql-connector-python',
        'pandas',
        'openpyxl'
    ],
    entry_points={
        'console_scripts': [
            'mysql-to-excel=mysql_to_excel.converter:convert_to_excel',
        ],
    },
)