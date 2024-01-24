from setuptools import setup, find_packages

setup(
    name='u2p',
    version='0.0.1',
    packages=find_packages(),
    install_requires=[
        'requests',
        'colorama',
        'ratelimit',
    ],
    entry_points={
        'console_scripts': [
            'u2p = u2p.main:main'
        ]
    },
    url='https://github.com/cyberduck404/u2p',
    license='MIT',
    author='pyscr1pt3r',
    author_email='re4son.t@yandex.com',
    description='Turn urls into profit',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown'
)