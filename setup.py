from setuptools import setup, find_packages

setup(
    name='bluebellutils',  
    version='0.1.0',  
    author='Marcio Bastos',  
    author_email='marcio.bastos@bluebellindex.com',
    description='A utility library for various client interfaces and utilities',
    long_description=open('README.md').read(),  
    long_description_content_type='text/markdown', 
    url='https://gitlab.com/bluebell-index/bluebellutils', 
    packages=find_packages(),  
    install_requires=[
        'azure-storage-blob',  # For Azure Blob Storage
        'redis',               # For Redis
        'requests',            # For HTTP requests
        'pika',                # For RabbitMQ (Pika)
        'injector'             # For Dependency Injection (Injector)
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.11',
)
