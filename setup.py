from setuptools import setup
import requests_github_oauth

setup(
    name='requests-github-oauth',
    version=requests_github_oauth.__version__,
    license='GNU Lesser General Public License',
    url='https://github.com/lukmdo/requests-github-oauth',
    author='lukmdo',
    author_email='me@lukmdo.com',
    description=requests_github_oauth.__about__,
    long_description=requests_github_oauth.__doc__,
    modules=['requests_github_oauth'],
    test_suite='tests',
    zip_safe=False,
)
