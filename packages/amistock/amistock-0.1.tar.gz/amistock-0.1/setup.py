from setuptools import setup, find_packages

setup(
    name='amistock',
    version='0.1',
    description='Python module to interact with stock data via Django API',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Ami Stock',
    author_email='amistockpro@gmail.com',
    url='https://github.com/amistock/amistock',
    packages=find_packages(),
    install_requires=[
        'requests',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    package_data={
        'amistock': ['examples/*.py'],  # Bao gồm các file ví dụ trong thư mục 'examples'
    },
)
