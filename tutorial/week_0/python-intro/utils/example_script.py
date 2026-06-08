# This script demonstrates importing from another module.
# It works when run directly from the utils/ directory:
#   cd utils && python example_script.py
#
# Note: this uses an absolute import (not a relative one like "from .example_module"),
# because this file is meant to be run as a standalone script, not as part of a package.
from example_module import average

a = 5
b = 10

average_number = average(a, b)
print(f"The average of {a} and {b} is {average_number}")