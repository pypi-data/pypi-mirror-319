from setuptools import setup, find_packages

setup(
    name='mpythonlinklib',
    version='0.0.1',
    author='TMiracleOW',
    author_email='1037085395@163.com',
    packages=find_packages(),
    description='Used for UDP control of labplus products',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='',
    license='MIT',
    install_requires=[
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)