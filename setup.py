from setuptools import setup

setup(
    name='stocktake',
    version='0.1',
    py_modules=['stocktake'],
    include_package_data=True,
    install_requires=[
        'click',
    ],
    entry_points='''
        [console_scripts]
        stocktake=stocktake:cli
    ''',
)