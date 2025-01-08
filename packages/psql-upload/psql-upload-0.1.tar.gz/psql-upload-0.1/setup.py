from setuptools import setup, find_packages

setup(
    name='psql-upload',  # The name of your package
    version='0.1',       # Version number
    packages=find_packages(),  # Automatically find all packages in your directory
    install_requires=[     # List your package dependencies
        'pandas',
        'sqlalchemy',
        'psycopg2',
        'pymysql',
    ],
    author='Prabhav Sharma',   # Your name
    author_email='prabhavs2004@gmail.com',  # Your email
    description='A simple utility for uploading data from CSV to PostgreSQL',  # Short description
    long_description=open('README.md').read(),  # Long description, typically from a README file
    long_description_content_type='text/markdown',  # Format of your long description
    url='https://github.com/Amalgamator04/sqlupload',  # URL to your project repo
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',  # Python version compatibility
)
