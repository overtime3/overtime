
# Overtime
![dev-test-suite](https://github.com/overtime3/overtime/actions/workflows/overtime-dev-test-suite.yml/badge.svg?branch=dev)  

## Test Methodology

> Recommended guide for unit testing in Python; [unittest](https://docs.python.org/3/library/unittest.html). Currently Overtime is using the built-in unittest package for all testing requirements.

> All tests are located in the [overtime/tests/](https://github.com/overtime3/overtime/tree/dev/overtime/tests) folder, with a file/directory structure that mirrors the main library. The idea is that all methods and classes in overtime are tested through mirror test methods/classes.
> The tests are imported through a series of init files. This allows access to the complete test suite through a single import of the library.

> Sample tests can be found at [test_graphs.py](https://github.com/overtime3/overtime/blob/dev/overtime/tests/components/test_graphs.py). It is important to note that in order for individual tests to be registered by the unittest module, they must begin with 'test_'.

> The test suite can be executed through [run.py](https://github.com/overtime3/overtime/blob/dev/overtime/tests/run.py).

> Automated testing is implemented through GitHub Actions. The workflow for the dev branch can be found at [overtime-dev-test-suite.yml](https://github.com/overtime3/overtime/blob/dev/.github/workflows/overtime-dev-test-suite.yml).
> This workflow executes the [run.py](https://github.com/overtime3/overtime/blob/dev/overtime/tests/run.py) file on pull requests *(recommended)* and pushs to the dev branch. This ensures that all tests are run for each change to the dev branch, ensuring the library does not regress as the codebase is updated. It is important that the test coverage of the library is maintained in order for the automated testing procedure to work as intended. Therefore, it is recommended that each functional contribution to the library is paired with sufficient tests of the new functionalities.
