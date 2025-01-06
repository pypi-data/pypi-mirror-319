from setuptools import setup, find_packages

setup(
    name="naplock",
    version="2.0.0",
    description='A cryptographic key pair generator for secure communication.',
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",  # Set this to 'text/markdown' if your README is in Markdown format
    author="Akinsunlade Marvelous",
    author_email='akinmarvelous2022@gmail.com',
    license='MIT',
    install_requires=[
    	'numpy'
    ],
    packages=find_packages(),
    include_package_data=True,  # Make sure you have 'include_package_data' set correctly
)
