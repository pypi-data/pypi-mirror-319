from setuptools import setup, find_packages

VERSION = '2.4.1'
DESCRIPTION = 'A key-value database'
LONG_DESCRIPTION = 'nahcrofDB is a key-value database designed to be extremely simple to get running and to use. Please note that at this current time there is no way to host the database, this simply interacts with an existing file'

# Setting up
setup(
    name="nahcrofDB",
    version=VERSION,
    author="Tyrae Paul",
    author_email="support@nahcrof.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    keywords=['database'],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
    ]
)
