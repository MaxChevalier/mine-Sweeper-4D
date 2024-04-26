#  If you need to run this as part of a test suite in pytest, remember to prepend the test functions with 'test_'
#  ```pip install pytest```
#  ```pytest test.py```

# current testing environments (in yml file): ubuntu_latest and python 3.8 ; widows_2019 and python 3.12


import pytest
import platform
import re
from packaging import version

# Constants for minimum required versions
minimum_python_version = '3.8'  # Minimum Python version
# minimum_glibc_version = '2.28'  # Minimum glibc version # OLD: to test under older ubuntus


def check_python_version(min_version):
    # Use version parsing for correct comparison
    current_version = version.parse(platform.python_version())
    min_version = version.parse(min_version)
    return current_version >= min_version

""" OLD: for testing under older ubuntus
def check_glibc_version(min_version):
    # Extract glibc version and use version parsing for comparison
    glibc_version_str = platform.libc_ver()[1]
    glibc_version = version.parse(re.findall(r'\d+\.\d+', glibc_version_str)[0])
    min_version = version.parse(min_version)
    return glibc_version >= min_version"""

def test_environment():
    # Assert both Python and glibc versions
    assert check_python_version(minimum_python_version), f"Python version must be >= {minimum_python_version}"
    #  assert check_glibc_version(minimum_glibc_version), f"glibc version must be >= {minimum_glibc_version}"

# The test_environment function will now perform all checks and the assertion failures will provide feedback directly.
