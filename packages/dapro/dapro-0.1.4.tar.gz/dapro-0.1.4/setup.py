from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='dapro',
    version='0.1.4',
    description='A library to simplify eval and file handling in Telegram bots.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Dipanshu',
    author_email='dipanshu0919@gmail.com',
    url='https://github.com/Dipanshu0919/dapro',
    packages=find_packages(where='dapro'),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
    ],
    license='GPL-3.0',
)
