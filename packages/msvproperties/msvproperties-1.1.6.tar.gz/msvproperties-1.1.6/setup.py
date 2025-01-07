from setuptools import setup, find_packages

setup(
    name='msvproperties',
    version='1.1.6',
    packages=find_packages(),
    license='MIT',
    install_requires=[
        'certifi>=2024.12.14,<2025',
        'charset-normalizer>=3.4.1,<4',
        'idna>=3.10,<4',
        'probableparsing==0.0.1',
        'python-crfsuite==0.9.11',
        'python-dotenv==1.0.1',
        'requests==2.32.3',
        'urllib3==2.3.0',
        'usaddress==0.5.11',
    ],
    python_requires='<4',
    description='A Library for using in our CRM',
    author='Alireza',
    author_email='alireza@msvproperties.net',
    url='https://github.com/alireza-msvproperties/msvproperties/',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.13',
        'License :: OSI Approved :: MIT License',
    ],
)
