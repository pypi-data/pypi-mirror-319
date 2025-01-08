from setuptools import setup, find_packages

setup(
    name='FatalMemoryLiar',  # Updated to match the name in the image
    version='1.3',
    packages=find_packages(where="FatalMemoryLiar"),  # Ensure the right directory is included
    install_requires=[
        'pymem>=1.4.0'
    ],
    description='A way to make python cheating easy like memory.dll from C#.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Fatal_Liar',
    author_email='Brandinrat@gmail.com',
    url='https://github.com/FatalLiar/memoryPY',  # Updated GitHub URL
)
