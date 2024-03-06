from setuptools import setup, find_packages

setup(
    name='nasa_process_lib',  
    version='0.1.0',  
    author='Marcio Bastos',  
    author_email='marciomacielbastos@hotmail.com',
    description='A utility library for various client interfaces and utilities',
    long_description=open('README.md').read(),  
    long_description_content_type='text/markdown', 
    url='https://github.com/marciomacielbastos/nasa_process_lib', 
    packages=find_packages(),  
    install_requires=[
        "earthaccess",
        "gdal",
        "requests",
        "rasterio",
        "injector"
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.10',
)
