from setuptools import setup, find_packages

setup(
    name='fbdl-core',
    version='0.0.4',
    author='AntonThomzz',
    author_email='antonthomzz@gmail.com',
    description='Modul untuk mengunduh video dari Facebook melalui terminal.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/AntonThomz/fbdl-core',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    entry_points={
        'console_scripts': [
            'fbdl=fbdl_core.fbdl:main'
        ],
    }
)