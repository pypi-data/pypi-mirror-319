from setuptools import setup, find_packages

setup(
    name='user_auth_boilerplate',
    version='0.1.0',
    description='A boilerplate for user authentication and management',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Vibgyor Technologies',
    author_email='info@vibgyortech.co',
    url='https://github.com/vibgyorTechBhaumik/fast-auth/',
    packages=find_packages(exclude=('templates', 'venv')),
    include_package_data=True,
    install_requires=[
        'fastapi==0.115.6',
        'pydantic==2.10.4',
        'bcrypt',
        'python-dotenv==1.0.1',
        'PyJWT==2.10.1',
        'SQLAlchemy==2.0.36',
        'boto3==1.35.91',
        'botocore==1.35.91',
        'passlib==1.7.4',
        'pydantic-settings==2.7.1',
    ],
    classifiers=[
        'Programming Language :: Python :: 3.8',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.8',
)
