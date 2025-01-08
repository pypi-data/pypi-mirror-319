# Copyright iris-grib contributors
#
# This file is part of iris-grib and is released under the BSD license.
# See LICENSE in the root of the repository for full licensing details.
"""Unit tests for the `iris_grib.save_grib2` function."""

# Import iris_grib.tests first so that some things can be initialised before
# importing anything else.
import iris_grib.tests as tests

from unittest import mock

import iris_grib


class TestSaveGrib2(tests.IrisGribTest):
    def setUp(self):
        self.cube = mock.sentinel.cube
        self.target = mock.sentinel.target
        func = "iris_grib.save_pairs_from_cube"
        self.messages = list(range(10))
        slices = self.messages
        side_effect = [zip(slices, self.messages, strict=False)]
        self.save_pairs_from_cube = self.patch(func, side_effect=side_effect)
        func = "iris_grib.save_messages"
        self.save_messages = self.patch(func)

    def _check(self, append=False):
        iris_grib.save_grib2(self.cube, self.target, append=append)
        self.save_pairs_from_cube.assert_called_once_with(self.cube)
        args, kwargs = self.save_messages.call_args
        self.assertEqual(len(args), 2)
        messages, target = args
        self.assertEqual(list(messages), self.messages)
        self.assertEqual(target, self.target)
        self.assertEqual(kwargs, dict(append=append))

    def test_save_no_append(self):
        self._check()

    def test_save_append(self):
        self._check(append=True)


if __name__ == "__main__":
    tests.main()
