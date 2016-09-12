from setuptools import setup
from os_shell import __version__

setup(
    name='os-shell',
    version=__version__,
    description="An interactive Command Line Shell for Openstack CLI",
    long_description="Interactive command shell for Openstack",
    url="https://github.com/bdastur/os-shell",
    author="Behzad Dastur",
    author_email="bdastur@gmail.com",
    license="MIT",
    packages=["os_shell"],
    classifier=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Intended Audience :: Developers',
        'License :: Apache Software License',
        'Topic :: Software Development :: Libraries',
        'Topic :: Utilities',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: POSIX :: Linux',
        'Operating System :: MacOS',
    ],
    keywords="openstack cli autocomplete syntax",
    zip_safe=False,
    entry_points={
        'console_scripts': [
            'os-shell = os_shell.main:run'
        ]
    },
    install_requires=['python-openstackclient',
                      'openstacksdk',
                      'prompt-toolkit',
                      'PyYAML',
                      'Pygments']
)

