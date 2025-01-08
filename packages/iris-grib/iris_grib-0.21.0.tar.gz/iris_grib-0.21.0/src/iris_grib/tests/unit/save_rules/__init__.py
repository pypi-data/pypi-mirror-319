# Copyright iris-grib contributors
#
# This file is part of iris-grib and is released under the BSD license.
# See LICENSE in the root of the repository for full licensing details.
"""Unit tests for the :mod:`iris_grib.grib_save_rules` module."""

# Import iris_grib.tests first so that some things can be initialised before
# importing anything else.
import iris_grib.tests  # noqa: F401
from unittest import mock

import numpy as np

from iris.coords import DimCoord
from iris.coord_systems import GeogCS
from iris.cube import Cube
from iris.fileformats.pp import EARTH_RADIUS as PP_DEFAULT_EARTH_RADIUS


class GdtTestMixin:
    """Some handy common test capabilities for grib grid-definition tests."""

    TARGET_MODULE = "iris_grib._save_rules"

    def setUp(self):
        # Patch the ecCodes of the tested module.
        self.mock_eccodes = self.patch(self.TARGET_MODULE + ".eccodes")

        # Fix the mock ecCodes to record key assignments.
        def codes_set_trap(grib, name, value):
            # Record a key setting on the mock passed as the 'grib message id'.
            grib.keys[name] = value

        self.mock_eccodes.codes_set = codes_set_trap
        self.mock_eccodes.codes_set_long = codes_set_trap
        self.mock_eccodes.codes_set_float = codes_set_trap
        self.mock_eccodes.codes_set_double = codes_set_trap
        self.mock_eccodes.codes_set_long_array = codes_set_trap
        self.mock_eccodes.codes_set_array = codes_set_trap

        # Create a mock 'grib message id', with a 'keys' dict for settings.
        self.mock_grib = mock.Mock(keys={})

        # Initialise the test cube and its coords to something barely usable.
        self.test_cube = self._make_test_cube()

    def _default_coord_system(self):
        return GeogCS(PP_DEFAULT_EARTH_RADIUS)

    def _default_x_points(self):
        # Define simple, regular coordinate points.
        return [1.0, 2.0, 3.0]

    def _default_y_points(self):
        return [7.0, 8.0]  # N.B. is_regular will *fail* on length-1 coords.

    def _make_test_cube(
        self, cs=None, x_points=None, y_points=None, coord_units="degrees"
    ):
        # Create a cube with given properties, or minimal defaults.
        if cs is None:
            cs = self._default_coord_system()
        if x_points is None:
            x_points = self._default_x_points()
        if y_points is None:
            y_points = self._default_y_points()

        x_coord = DimCoord(
            x_points, long_name="longitude", units=coord_units, coord_system=cs
        )
        y_coord = DimCoord(
            y_points, long_name="latitude", units=coord_units, coord_system=cs
        )
        test_cube = Cube(np.zeros((len(y_points), len(x_points))))
        test_cube.add_dim_coord(y_coord, 0)
        test_cube.add_dim_coord(x_coord, 1)
        return test_cube

    def _check_key(self, name, value):
        # Test that a specific grib key assignment occurred.
        msg_fmt = 'Expected grib setting "{}" = {}, got {}'
        found = self.mock_grib.keys.get(name)
        if found is None:
            self.assertEqual(0, 1, msg_fmt.format(name, value, "((UNSET))"))
        else:
            self.assertArrayEqual(found, value, msg_fmt.format(name, value, found))

    def _check_scanmode(self, x_direction, y_direction):
        expected = 0
        if x_direction < 0:
            # "bit 1" set if x scans negatively
            expected |= 0x80
        if y_direction >= 0:
            # "bit 2" set if y does *not* scan negatively
            expected |= 0x40
        self._check_key("scanningMode", expected)
