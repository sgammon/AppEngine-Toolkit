"""
Generic Test case
"""
__docformat__ = 'restructuredtext'

import os
import sys
import re
import unittest
import doctest
import zc.buildout.testing
from zope.testing import renormalizing

current_dir = os.path.abspath(os.path.dirname(__file__))

normalize_version1 = (re.compile('= [0-9a-zA-Z -_]+([.][0-9a-zA-Z-_]+)+'), '= N.N')
normalize_version2 = (re.compile('(#[^ ]*?) [0-9a-zA-Z -_]+([.][0-9a-zA-Z-_]+)+'), '\\1 N.N')

def doc_suite(test_dir, setUp=zc.buildout.testing.buildoutSetUp, tearDown=zc.buildout.testing.buildoutTearDown, globs=None):
    """Returns a test suite, based on doctests found in /doctest."""
    suite = []
    if globs is None:
        globs = globals()

    flags = (doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE |
             doctest.REPORT_ONLY_FIRST_FAILURE)

    package_dir = os.path.split(test_dir)[0]
    if package_dir not in sys.path:
        sys.path.append(package_dir)

    doctest_dir = test_dir

    # filtering files on extension
    docs = [os.path.join(doctest_dir, doc) for doc in
            os.listdir(doctest_dir) if doc.endswith('.txt')]

    for test in docs:
        suite.append(doctest.DocFileSuite(test, optionflags=flags, 
                                          globs=globs, setUp=setUp, 
                                          tearDown=tearDown,
                                          checker=renormalizing.RENormalizing([normalize_version1, normalize_version2]),
                                          module_relative=False))

    return unittest.TestSuite(suite)

def test_suite():
    """returns the test suite"""
    return doc_suite(current_dir)

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')


