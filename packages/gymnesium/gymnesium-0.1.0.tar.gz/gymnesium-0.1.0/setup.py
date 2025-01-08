"""The setup script for installing and distributing the gymnesium package."""
import os
from setuptools import setup


# set the compiler for the C++ framework
os.environ['CC'] = 'g++'
os.environ['CCX'] = 'g++'


# read the contents from the README file
with open('README.md') as README_file:
    README = README_file.read()


setup(
    name='gymnesium',
    version='0.1.0',
    description='An NES Gymnasium Environment',
    long_description=README,
    long_description_content_type='text/markdown',
    keywords='NES Emulator OpenAI-Gym Gymnasium',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: POSIX :: Linux',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: C++',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Topic :: Games/Entertainment',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: System :: Emulators',
    ],
    url='https://github.com/Hal609/GymNESium',
    author='Hal Kolb',
    author_email='hal@kolb.co.uk',
    license='MIT',
    zip_safe=False,
    install_requires=[
        'numpy>=1.18.5',
        'cynes>=0.1.0',
        'gymnasium>=1.0.0'
    ],
)