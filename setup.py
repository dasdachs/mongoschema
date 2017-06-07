from distutils.core import setup


setup(
    name='Mongoschema',
    version='0.1dev',
    author='Jani Šumak',
    author_email='jani.sumak@gmail.com',
    url='https://github.com/dasdachs/mongoschema',
    packages=['mongoschema',],
    license='MIT',
    description='MongoDB schema analyzer',
    long_description=open('README.rst').read(),
    classifiers=[
          'Development Status :: 3 - Alpha',
          'Environment :: Console',
          'Intended Audience :: Developers',
          'Operating System :: MacOS :: MacOS X',
          'Operating System :: Microsoft :: Windows',
          'Operating System :: POSIX',
          'Operating System :: Unix',
          # 'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.3',
          'Programming Language :: Python :: 3.4',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python',
          'Topic :: Database',
          'Topic :: Software Development :: Documentation'
    ],
    keywords=[
        "MongoDB", "schema", "database tools",
    ],

    # Requirements 
    install_requires=[
        "pymongo >= 3.4",
    ],

    # CLI tool
    entry_points={
        'console_scripts':""
    },
)
