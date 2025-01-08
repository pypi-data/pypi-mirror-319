# anchorscad-test-tools

This package provides a test helper for comparing two iterables based on an
expectation function. It provides more information about the difference
between the two iterables.

The module `anchorscad_lib.test_tools` is the main module in this package.
The `anchorscad_lib` namespace is used by a number of Anchorscad packages.

## Installation

```
pip install anchorscad-test-tools
```

## Usage

```
import unittest
from anchorscad_lib.test_tools import iterable_assert

class TestMyThing(unittest.TestCase):
    def test_almost_same(self):
        iterable_assert(self.assertAlmostEqual, VALUESA, VALUESB, places=3)
```

This is not particularly revolutionary, but it is used by a number of Anchorscad
tests in now different packages which required this to be extracted into a
separate package.

