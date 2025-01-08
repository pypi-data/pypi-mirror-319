from setuptools import setup, find_packages

setup(
    name='shareithub',
    version='1.0.0',
    packages=find_packages(),
    description='This intro from SHARE IT HUB',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='SHARE IT HUB',
    author_email='',
    url='https://github.com/shareithub?tab=repositories',
    license='MIT',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
