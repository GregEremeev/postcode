from setuptools import setup, find_packages


setup(
    name='postcode',
    author='Greg Eremeev',
    author_email='gregory.eremeev@gmail.com',
    version='0.1.0',
    license='BSD-3-Clause',
    url='https://github.com/GregEremeev/postcode',
    description='Library to validate postcodes',
    packages=find_packages(),
    extras_require={'dev': ('pdbpp>=0.10.2', 'ipdb>=0.13.3', 'pytest>=5.4.3')},
    entry_points={
        'console_scripts': ['validate_uk_postcode=postcode.uk:main'],
    },
    classifiers=(
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: Implementation :: CPython'
    ),
    zip_safe=False,
    include_package_data=True
)
