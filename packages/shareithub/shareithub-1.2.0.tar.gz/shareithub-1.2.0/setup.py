from setuptools import setup, find_packages

setup(
    name="shareithub",
    version="1.2.0",
    packages=find_packages(),
    author="SHARE IT HUB",
    author_email="",
    description="Don't forget to join us at: SHARE IT HUB",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/shareithub",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)

