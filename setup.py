from setuptools import setup, find_packages

setup(
    name='scoper',
    version='1.0.0',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    include_package_data=True,
    install_requires=[
        'click',
        'questionary',
        'playwright',
        'markdown',
        'jinja2',
        'pyyaml',
        'rich'
    ],
    entry_points='''
        [console_scripts]
        scoper=scoper.cli:cli
    ''',
)
