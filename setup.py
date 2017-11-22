from setuptools import setup

setup(
    name='needle_app',
    packages=['needle_app'],
    include_package_data=True,
    install_requires=[
        'flask',
        'flask-admin',
        'flask-login',
        'flask-mail',
        'flask-sqlalchemy',
        'flask-wtf'
    ],
)
