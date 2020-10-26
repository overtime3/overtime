
def run(verbosity=2):
    """
        Run Overtime test suite.

        Parameter(s):
        -------------
        verbose : Integer
            Controls level of detail of reports.


        Returns:
        --------
        None, performs unitest.main() and reports to standard output.
    """
    import unittest
    unittest.main(verbosity=verbosity)


if __name__ == "__main__":
    from overtime.tests import *
    run()
