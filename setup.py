##------------------------------------------------------------
## API client for http://www.statweb.provincia.tn.it/
##------------------------------------------------------------

import sys
from pkg_resources import normalize_path
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand

version = '0.1-alpha'

install_requires = [
    'requests',
]

tests_require = [
    'pytest',
    'pytest-pep8',
    'pytest-cov',
]

extra = {}
if sys.version_info >= (3,):
    extra['use_2to3'] = True


class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = [
            '--ignore=build',
            '--cov=pat_statweb_client',
            '--cov-report=term-missing',
            '--pep8',
            '.']
        self.test_suite = True

    def run_tests(self):
        from pkg_resources import _namespace_packages
        import pytest

        # Purge modules under test from sys.modules. The test loader will
        # re-import them from the build location. Required when 2to3 is used
        # with namespace packages.
        if sys.version_info >= (3,) and \
                getattr(self.distribution, 'use_2to3', False):
            module = self.test_args[-1].split('.')[0]
            if module in _namespace_packages:
                del_modules = []
                if module in sys.modules:
                    del_modules.append(module)
                module += '.'
                for name in sys.modules:
                    if name.startswith(module):
                        del_modules.append(name)
                map(sys.modules.__delitem__, del_modules)

            ## Run on the build directory for 2to3-built code..
            ei_cmd = self.get_finalized_command("egg_info")
            self.test_args = [normalize_path(ei_cmd.egg_base)]

        errno = pytest.main(self.test_args)
        sys.exit(errno)


setup(
    name='PAT_StatWeb_Client',
    version=version,
    packages=find_packages(),
    url='http://github.com/opendatatrentino/pat_statweb_client',
    license='BSD License',
    author='Samuele Santi',
    author_email='samuele@samuelesanti.com',
    description='Client for the http://statweb.provincia.tn.it',
    long_description='Client for the http://statweb.provincia.tn.it',
    install_requires=install_requires,
    tests_require=tests_require,
    test_suite='datapub.tests',
    classifiers=[
        "License :: OSI Approved :: BSD License",
        "Development Status :: 1 - Planning",
        "Programming Language :: Python :: 2.7",
    ],
    package_data={'': ['README.md', 'LICENSE']},
    cmdclass={'test': PyTest},
    **extra
)
