from setuptools import setup, find_packages

setup(
    name='autocleanser',
    version='0.3.1',
    packages=find_packages(),
    install_requires=[],  # List dependencies if any
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Mukilan M',
    description='auto cleaning the data with easy user interface',
    python_requires='>=3.6',  # Ensure compatibility with Python 3.6 and above
)
