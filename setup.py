import setuptools

with open('README.md') as file:
    long_description = file.read()

requirements = 'feedparser', 'jinja2', 'gnureadline'
setuptools.setup(
    name='vehicular',
    version='0.1.0',
    author='Alexander Potts',
    author_email='alexander.potts@gmail.com',
    description='a craigslist vehicle search cli app',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/jakkso/vehicular',
    packages=setuptools.find_packages(),
    install_requires=requirements,
    include_package_data=True,
    data_files=[('vehicular/templates', ['vehicular/templates/base.txt',
                                         'vehicular/templates/base.html',
                                         'vehicular/templates/_listing.html'])],
    classifiers=(
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: MacOS",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3 :: Only ",
        "Topic :: Utilities",
    ),
    entry_points={'console_scripts': ['vehicular = vehicular.__main__:launch']},
)
