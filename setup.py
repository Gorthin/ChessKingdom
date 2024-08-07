from setuptools import setup, find_packages

setup(
    name='Chess_kingdom',
    version='0.1.0',
    description='The game allows players to play chess',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Adrian Janiak',
    author_email='adrian88janiak@gmail.com',
    url='https://github.com/Gorthin/ChessKingdom',
    packages=find_packages(),
    package_dir={
        '': 'src'
    },
    install_requires=[
        'pygame>=2.6.0'
    ],
    license='MIT',
    classifiers=[
        'Development Status :: 1 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',
    ],
    keywords='przykladowe slowa kluczowe',
)